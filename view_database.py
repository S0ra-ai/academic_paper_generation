#!/usr/bin/env python3
"""
数据库表内容查看工具

功能：
1. 查看reports表中的所有报告记录
2. 以友好的格式显示报告信息
3. 支持分页查看
"""

import os
import sys
import argparse
from datetime import datetime

# 添加backend目录到Python路径
sys.path.insert(0, os.path.abspath('./backend'))

# 导入应用和数据库
from app.app import app
from app.models import db, Report

def view_reports(limit=10, offset=0):
    """
    查看reports表中的报告记录
    
    Args:
        limit (int): 每页显示的记录数
        offset (int): 偏移量
    """
    with app.app_context():
        try:
            # 查询数据库中的报告记录
            reports = Report.query.order_by(Report.id.desc()).limit(limit).offset(offset).all()
            total = Report.query.count()
            
            print("="*80)
            print("📊 学术报告数据库记录")
            print("="*80)
            print(f"总记录数: {total}")
            print(f"当前显示: 第 {offset+1}-{min(offset+limit, total)} 条记录")
            print("="*80)
            
            if not reports:
                print("没有找到报告记录")
                return
            
            # 显示报告信息
            for report in reports:
                print(f"\n报告ID: {report.id}")
                print(f"研究主题: {report.topic}")
                print(f"报告标题: {report.title}")
                print(f"文件名: {report.filename}")
                print(f"文件路径: {report.file_path}")
                print(f"字数: {report.word_count} 字符")
                print(f"状态: {report.status}")
                print(f"创建时间: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"更新时间: {report.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print("-"*80)
            
        except Exception as e:
            print(f"查询数据库失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='查看学术报告数据库表内容')
    parser.add_argument('--limit', type=int, default=10, help='每页显示的记录数')
    parser.add_argument('--offset', type=int, default=0, help='偏移量')
    
    args = parser.parse_args()
    
    view_reports(args.limit, args.offset)

if __name__ == "__main__":
    main()