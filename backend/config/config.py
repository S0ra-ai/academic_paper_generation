import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 'yes']
    # 上传文件大小限制 - 100MB
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', '104857600'))
    
    # 数据库配置 - MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 
        'mysql+pymysql://report_user:report_password@localhost/report_make')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ['true', '1', 'yes']
    
    # API密钥配置
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY', '')
    ACADEMIC_EMAIL = os.environ.get('ACADEMIC_EMAIL', '')
    
    # LLM配置
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'google/gemini-3-pro-preview')
    LLM_TEMPERATURE = float(os.environ.get('LLM_TEMPERATURE', '0.0'))
    LLM_MAX_TOKENS = int(os.environ.get('LLM_MAX_TOKENS', '32768'))
    LLM_TIMEOUT = int(os.environ.get('LLM_TIMEOUT', '600'))  # 增加到10分钟
    
    # 本地文档配置
    KNOWLEDGE_DIR = os.environ.get('KNOWLEDGE_DIR', './database')
    SAVE_DIR = os.environ.get('SAVE_DIR', './reports')
    
    # 模板配置
    TEMPLATES_DIR = os.environ.get('TEMPLATES_DIR', './templates')
    
    # 搜索配置
    SEARCH_LIMIT = int(os.environ.get('SEARCH_LIMIT', '6'))
    
    #Embedding模型配置
    EMBEDDING_MODEL_NAME = os.environ.get('EMBEDDING_MODEL_NAME', './cache/huggingface/models--sentence-transformers--all-MiniLM-L6-v2')
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass