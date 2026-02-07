import os
import time
import json
import logging
from typing import Dict
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential

from app.services.llm_service import LLMService
from app.services.search_service import UnifiedAcademicSearcher
from app.services.local_doc_service import LocalDocManager
from app.models import db, Report

# 加载配置
from config.config import Config

class ReportGenerator:
    def __init__(self):
        self.llm = LLMService()
        self.searcher = UnifiedAcademicSearcher()
        self.search_limit = Config.SEARCH_LIMIT
        
        # 尝试初始化本地RAG系统，如果失败则跳过
        try:
            self.local_rag = LocalDocManager()
            self.local_rag.build_index()
            logging.info("✅ 本地RAG系统初始化成功")
        except Exception as e:
            logging.warning(f"⚠️ 本地RAG系统初始化失败: {e}")
            logging.info("📌 将使用网络搜索结果生成报告")
            self.local_rag = None
        
        # 不再需要本地报告存储目录，所有报告只存储在前端localStorage中

    def generate_report(self, topic: str, local_rag=None, template: str = "") -> Dict[str, str]:
        logging.info(f"💡 [阶段 1] 分析与翻译: {topic}")
        queries = self.llm.translate_to_keywords(topic)
        logging.info(f"   🎯 搜索策略: {json.dumps(queries, ensure_ascii=False)}")
        
        logging.info(f"🔍 [阶段 2] 多源并发检索 (含 Crossref/OpenAlex/ArXiv/S2)...")
        web_results = self.searcher.run_ensemble_search(queries, limit=self.search_limit)
        
        local_context = ""
        # 使用传入的临时知识库实例（如果提供），否则使用默认实例
        rag_instance = local_rag if local_rag else self.local_rag
        if rag_instance:
            local_context = rag_instance.query(topic)
        
        # 构建上下文
        context_str = ""
        
        # 优先使用本地知识库内容（权重更高）
        if local_context:
            context_str += f"【Local Knowledge Base】\n{local_context}\n\n"
        
        context_str += "【Web References】\n"
        for i, r in enumerate(web_results[:18], 1): 
            context_str += f"[{i}] Title: {r['title']}\n    Source: {r['source']} ({r['year']})\n    Authors: {r['authors']}\n    Abstract: {r['snippet']}\n    URL: {r['link']}\n\n"

        logging.info(f"✍️ [阶段 3] 深度报告生成中 (Context: {len(context_str)} chars)...")
        
        # 读取模板内容（如果提供）
        template_content = ""
        if template:
            # 使用绝对路径确保能找到模板文件
            template_path = os.path.abspath(os.path.join(Config.TEMPLATES_DIR, template))
            logging.info(f"📁 尝试读取模板文件: {template_path}")
            if os.path.exists(template_path):
                try:
                    template_text = []
                    file_ext = os.path.splitext(template_path)[1].lower()
                    logging.info(f"📋 模板文件格式: {file_ext}")
                    
                    if file_ext == '.docx':
                        # 读取DOCX文件内容
                        import docx
                        doc = docx.Document(template_path)
                        for para in doc.paragraphs:
                            if para.text.strip():
                                template_text.append(para.text)
                    elif file_ext == '.doc':
                        # 读取DOC文件内容，使用antiword工具提取文本
                        import subprocess
                        
                        try:
                            # 使用antiword提取.doc文件内容
                            result = subprocess.run(
                                ['antiword', template_path],
                                capture_output=True,
                                text=True,
                                check=True
                            )
                            doc_content = result.stdout
                            
                            # 将提取的文本按换行符分割成段落
                            paragraphs = doc_content.split('\n')
                            for para in paragraphs:
                                text = para.strip()
                                if text:
                                    template_text.append(text)
                            
                            logging.info(f"✅ 使用antiword成功提取.doc文件内容，共 {len(doc_content)} 字符")
                        except subprocess.CalledProcessError as e:
                            logging.error(f"⚠️  使用antiword提取.doc文件失败: {e}")
                            # 尝试使用textract作为备选方案
                            try:
                                import textract
                                doc_content = textract.process(template_path).decode('utf-8')
                                paragraphs = doc_content.split('\n')
                                for para in paragraphs:
                                    text = para.strip()
                                    if text:
                                        template_text.append(text)
                                logging.info(f"✅ 使用textract成功提取.doc文件内容，共 {len(doc_content)} 字符")
                            except Exception as fallback_e:
                                logging.error(f"⚠️  备选方案处理.doc文件也失败: {fallback_e}")
                                template_content = ""
                    else:
                        logging.error(f"⚠️  不支持的模板文件格式: {file_ext}")
                        template_content = ""
                    
                    template_content = "\n".join(template_text)
                    logging.info(f"✅ 已读取模板文件: {template} (共 {len(template_content)} 字符)")
                except Exception as e:
                    logging.error(f"⚠️  读取模板文件失败: {e}")
                    # 详细的错误信息，包括文件路径和实际存在的文件
                    import traceback
                    logging.error(f"🚨 模板读取详细错误: {traceback.format_exc()}")
                    # 列出Templates目录下的文件，帮助调试
                    templates_dir = os.path.dirname(template_path)
                    if os.path.exists(templates_dir):
                        files = os.listdir(templates_dir)
                        logging.info(f"📋 Templates目录下的文件: {files}")
                    else:
                        logging.error(f"📋 Templates目录不存在: {templates_dir}")
                    template_content = ""
            else:
                logging.error(f"⚠️  模板文件不存在: {template_path}")
                # 列出templates目录下的文件，帮助调试
                templates_dir = os.path.dirname(template_path)
                if os.path.exists(templates_dir):
                    files = os.listdir(templates_dir)
                    logging.info(f"📋 Templates目录下的文件: {files}")
                else:
                    logging.error(f"📋 Templates目录不存在: {templates_dir}")

        date_str = datetime.now().strftime("%Y-%m")
        
        # 构建带有模板的prompt
        template_requirement = ""
        if template_content:
            template_requirement = f"\n\n**Template Requirements:**\n**CRITICAL: You MUST strictly follow the structure, format, sections, and wording of the provided template. Your entire report MUST match the template's structure exactly.**\nIntegrate the research content into the template framework without modifying the template's structure. Here's the template content:\n\n{template_content}\n\n**IMPORTANT: Do not deviate from the template structure. Do not add any new sections. Do not remove any sections from the template. Use the template as a framework and fill in the content.**\n"
        
        prompt = f"""You are a Principal Investigator (PI) writing a comprehensive review paper on "{topic}".
Writing Date: {date_str}

**Source Material:**
{context_str}

**Requirements:**
1. **Format:** Academic Markdown. strict LaTeX math ($...$).
2. **Length:** Extremely detailed and comprehensive. Aim for 8000-10000 Chinese characters.
3. **Evidence:** 
   - **优先引用本地知识库内容**，增加其在报告中的权重
   - 每一个论点都必须引用提供的来源，**严格使用上下文中的原始编号**（例如：如果上下文中是[5]，则只能引用[5]，不能更改编号）
   - **本地知识库资源引用标记**：使用大于20的数字编号（例如：[21], [22]）
   - **网络搜索资源引用标记**：使用1-20的数字编号（例如：[1], [15]）
4. **Structure:**
   - **Abstract**: Concise summary.
   - **Introduction**: Market drivers & theoretical background.
   - **Mechanism & Theory**: Use LaTeX equations to explain the physics/chemistry.
   - **State-of-the-Art (SOTA)**: Compare technical routes found in the sources.
   - **Critical Comparisons**: **MUST** include a Markdown Table comparing performance metrics (extracted from sources).
   - **Challenges & Future**: What is missing in current research?
   - **References**: 
     - 必须列出所有引用的文献，**严格按照上下文中的原始编号顺序排列**
     - **明确区分本地知识库和网络搜索资源**，使用不同的章节或标记
     - 本地知识库资源：使用"[本地文件]"前缀，格式为：[编号] [本地文件] 文件名 - Local Knowledge Base
     - 网络搜索资源：使用正常格式，例如：[编号] 作者. 标题. 来源 (年份). URL
     - **参考文献列表中的编号必须与正文中的引用完全一致**，不能更改编号或顺序

{template_requirement}

Write the report now in Chinese (Professional Scientific Tone), except for English terminology."""
        msg = [SystemMessage(content="You are a rigorous scientific writer."), HumanMessage(content=prompt)]
        
        try:
            content = self.llm.chat(msg)
            
            # 使用用户输入的研究主题作为文件名，先清理特殊字符
            import re
            timestamp = int(time.time())
            safe_topic = re.sub(r'[\/*?:"<>|]', '_', topic)  # 替换Windows和Linux的非法字符
            safe_topic = safe_topic.strip()
            if not safe_topic:
                safe_topic = f"report_{timestamp}"
            filename = f"{safe_topic}.md"
            
            logging.info(f"✅ 报告已生成: {filename} (仅在前端localStorage中存储)")
            logging.info(f"📄 字数: {len(content)}")
            
            # 不返回实际文件路径，只返回虚拟路径
            
            # 不再保存报告到数据库，仅返回生成的报告内容
            logging.info(f"✅ 报告生成成功，将通过前端保存到localStorage")
            
            return {
                "status": "success",
                "filename": filename,
                "filepath": None,  # 不再保存到文件系统，返回None
                "content": content,
                "word_count": len(content)
            }
        except KeyboardInterrupt:
            logging.info("🛑 用户停止生成")
            return {
                "status": "interrupted",
                "message": "用户停止生成"
            }
        except Exception as e:
            logging.error(f"❌ 报告生成失败: {e}")
            return {
                "status": "error",
                "message": str(e)
            }