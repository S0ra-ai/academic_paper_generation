import os
import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# 初始化数据库实例
db = SQLAlchemy()

class KnowledgeBase(db.Model):
    """知识库表模型 - 用于存储各种文本类型的文件"""
    __tablename__ = 'knowledge_base'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    filename = db.Column(db.String(255), nullable=False)  # 文件名
    file_path = db.Column(db.String(500), nullable=False)  # 文件路径
    file_type = db.Column(db.String(20), nullable=False)  # 文件类型（md, txt, doc等）
    content = db.Column(db.Text, nullable=False)  # 文件内容
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    metadata_json = db.Column(db.Text, nullable=True)  # 文件元数据（JSON格式）
    
    def __repr__(self):
        return f'<KnowledgeBase {self.filename}>'

class Report(db.Model):
    """报告表模型 - 用于存储生成的报告"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    topic = db.Column(db.String(255), nullable=False)  # 报告主题
    title = db.Column(db.String(255), nullable=False)  # 报告标题
    content = db.Column(db.Text, nullable=False)  # 报告内容
    filename = db.Column(db.String(255), nullable=False)  # 报告文件名
    file_path = db.Column(db.String(500), nullable=False)  # 报告文件路径
    word_count = db.Column(db.Integer, nullable=False)  # 报告字数
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    status = db.Column(db.String(50), nullable=False, default='completed')  # 报告状态
    
    def __repr__(self):
        return f'<Report {self.title}>'