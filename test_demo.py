#!/usr/bin/env python3
"""
学术报告生成系统测试Demo

功能：
1. 用户输入研究主题
2. 调用后端API生成学术报告
3. 在数据库中存储报告信息
4. 返回生成的报告内容和存储路径
"""

import requests
import json
import time
import os

def generate_report(topic):
    """
    调用后端API生成学术报告
    
    Args:
        topic (str): 研究主题
    
    Returns:
        dict: 生成结果
    """
    # 后端API地址
    api_url = "http://localhost:5000/api/generate-report"
    
    # 请求数据
    payload = {
        "topic": topic
    }
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"\n正在生成关于 '{topic}' 的学术报告...")
        print("请稍候，这可能需要几分钟时间...")
        
        # 发送POST请求
        response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=300)
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"API调用失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接或稍后重试")
        return None
    except requests.exceptions.ConnectionError:
        print("无法连接到后端服务，请确保服务已启动")
        return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

def display_result(result):
    """
    显示生成结果
    
    Args:
        result (dict): 生成结果
    """
    if not result or result.get("status") != "success":
        print("\n报告生成失败！")
        if result:
            print(f"错误信息: {result.get('message', '未知错误')}")
        return
    
    print(f"\n✅ 报告生成成功！")
    print(f"📄 报告标题: {result.get('title', result.get('filename'))}")
    print(f"📁 保存路径: {result.get('filepath')}")
    print(f"📊 字数统计: {result.get('word_count', 0)} 字符")
    print(f"📅 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 询问用户是否查看报告内容
    view_content = input("\n是否查看报告前1000个字符的内容？(y/n): ")
    if view_content.lower() == 'y':
        print("\n" + "="*50)
        print("报告内容预览:")
        print("="*50)
        content = result.get('content', '')
        print(content[:1000] + "...")
        print("="*50)
    
    print("\n📝 提示：报告已自动保存到数据库中，您可以通过数据库查询历史报告")

def main():
    """
    主函数
    """
    print("="*60)
    print("🔬 学术报告生成系统测试Demo")
    print("="*60)
    print("该系统可以根据您输入的研究主题，自动生成高质量的学术报告。")
    print("报告将包含多源检索结果和深度分析内容，并自动保存到数据库。")
    print("="*60)
    
    # 获取用户输入的研究主题
    while True:
        topic = input("\n请输入您的研究主题: ")
        if topic.strip():
            break
        print("❌ 研究主题不能为空，请重新输入")
    
    # 调用生成函数
    result = generate_report(topic.strip())
    
    # 显示结果
    display_result(result)
    
    print("\n" + "="*60)
    print("🎉 测试完成！")
    print("="*60)

if __name__ == "__main__":
    main()