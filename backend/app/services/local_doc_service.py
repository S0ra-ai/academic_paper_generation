import os
import logging
from typing import List, Dict
from config.config import Config
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pdf2docx import Converter
# 导入数据库模型和app对象
from app.models import db, KnowledgeBase
from app.app import app

class LocalDocManager:
    """本地文档管理：负责加载、分割和检索本地知识库"""
    def __init__(self):
        # 将知识库目录转换为绝对路径，避免相对路径问题
        self.knowledge_dir = os.path.abspath(Config.KNOWLEDGE_DIR)
        self.vector_db = None
        self.embeddings = None
        # 初始化embedding模型（使用本地已下载的模型）
        self._init_embeddings()
        logging.info("📌 本地RAG系统初始化完成")

    def _init_embeddings(self):
        try:
            # 使用用户指定的本地模型绝对路径
            local_model_path = Config.EMBEDDING_MODEL_NAME
            
            # 检查本地模型路径是否存在
            if not os.path.exists(local_model_path):
                logging.error(f"❌ 本地模型路径不存在: {local_model_path}")
                self.embeddings = None
                return
            
            # 使用本地模型路径初始化embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=local_model_path,
                cache_folder="./.cache/huggingface",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            logging.info("✅ 本地 Embedding 模型加载成功")
        except Exception as e:
            logging.error(f"❌ 本地 Embedding 模型加载失败: {e}")
            self.embeddings = None
            logging.info("📌 将跳过本地RAG功能")

    def build_index(self, uploaded_files: List[str] = None, use_temp_storage: bool = True):
        if not self.embeddings or not os.path.exists(self.knowledge_dir): return
        
        # 没有上传文件时不执行任何操作（不再自动扫描）
        if not uploaded_files:
            logging.info("📋 没有需要处理的上传文件，跳过知识库构建")
            return
        
        documents = []
        temp_files = [] if use_temp_storage else []
        logging.info(f"📂 处理上传的知识库文件: {uploaded_files} (临时存储: {use_temp_storage})")
        
        for filename in uploaded_files:
            path = os.path.join(self.knowledge_dir, filename)
            try:
                # 获取文件扩展名（处理只有扩展名的情况，如'docx'）
                _, ext = os.path.splitext(filename)
                if not ext:
                    # 如果没有点号，将整个文件名视为扩展名
                    ext = filename
                else:
                    # 去除点号
                    ext = ext[1:]
                ext = ext.lower()
                
                # 根据扩展名选择加载器
                if ext == 'pdf':
                    # 先检查文件是否存在
                    if not os.path.exists(path):
                        logging.error(f"❌ 文件不存在: {path}")
                        continue
                    
                    try:
                        # 直接使用PyPDFLoader加载PDF文件，无需转换为Word
                        logging.info(f"📝 直接加载PDF文件: {filename}")
                        loader = PyPDFLoader(path)
                        logging.info(f"✅ PDF文件加载成功: {filename}")
                    except Exception as e:
                        logging.error(f"❌ 加载PDF文件失败: {e}")
                        # 加载失败，跳过该文件
                        continue
                elif ext == 'txt':
                    loader = TextLoader(path, encoding='utf-8')
                elif ext == 'md':
                    loader = TextLoader(path, encoding='utf-8')
                elif ext == 'docx':
                    loader = Docx2txtLoader(path)  # 支持docx格式
                elif ext == 'doc':
                    loader = UnstructuredWordDocumentLoader(path)  # 支持doc格式
                else: 
                    logging.warning(f"❌ 不支持的文件类型: {filename} (扩展名: {ext})")
                    continue
                
                docs = loader.load()
                for d in docs:
                    d.metadata['source'] = filename
                    d.metadata['path'] = path
                    d.metadata['temp'] = use_temp_storage
                documents.extend(docs)
                
                # 记录临时文件路径，用于后续清理
                if use_temp_storage:
                    temp_files.append(path)
            except Exception as e:
                logging.error(f"❌ 加载文件 {filename} 失败: {e}")
        
        if documents:
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
            split_docs = splitter.split_documents(documents)
            self.vector_db = FAISS.from_documents(split_docs, self.embeddings)
            logging.info(f"✅ 本地库建立完成，共 {len(split_docs)} 文本块")
            
            # 仅在非临时模式下保存到数据库
            if not use_temp_storage:
                try:
                    with app.app_context():
                        # 先清空现有数据
                        KnowledgeBase.query.delete()
                        
                        # 存储文档
                        for doc in documents:
                            # 获取文件类型
                            file_ext = os.path.splitext(doc.metadata['path'])[1][1:]
                            
                            # 创建知识库记录
                            knowledge_entry = KnowledgeBase(
                                filename=doc.metadata['source'],
                                file_path=doc.metadata['path'],
                                file_type=file_ext,
                                content=doc.page_content,
                                file_size=os.path.getsize(doc.metadata['path'])
                            )
                            db.session.add(knowledge_entry)
                        
                        db.session.commit()
                        logging.info(f"✅ 知识库数据已保存到数据库，共 {len(documents)} 条记录")
                except Exception as e:
                    logging.error(f"❌ 保存知识库到数据库失败: {e}")
                    db.session.rollback()
            else:
                logging.info("📌 临时知识库模式，跳过数据库存储")
        
        return temp_files

    def query(self, text: str) -> str:
        if not self.vector_db: return ""
        try:
            docs = self.vector_db.similarity_search(text, k=5)
            result = []
            for i, d in enumerate(docs, 1):
                source = d.metadata.get('source', 'Unknown')
                content = d.page_content[:400].replace(chr(10), ' ').strip()
                result.append(f"[{i+20}] Title: {source}\n    Source: Local Knowledge Base\n    Content: {content}...")
            return "\n\n".join(result)
        except: return ""