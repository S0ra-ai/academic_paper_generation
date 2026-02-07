import os
import sys
from flask import Flask
from flask_migrate import Migrate

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入应用和数据库
from app.app import app
from app.models import db

# 初始化迁移工具
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表（如果不存在）
        db.create_all()
        print("数据库表结构创建完成！")
        
        # 提示用户如何使用迁移功能
        print("\n📚 数据库迁移使用指南：")
        print("1. 初始化迁移仓库: flask db init")
        print("2. 创建迁移脚本: flask db migrate -m \"迁移描述\"")
        print("3. 应用迁移: flask db upgrade")
        print("4. 回滚迁移: flask db downgrade")
    
    print("\n✅ 数据库初始化完成！")