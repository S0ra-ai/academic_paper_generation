import requests
import os
import time

# 创建简单的测试文件
test_content = "这是临时知识库的测试内容，应该只在本次报告中出现。"
test_file_path = "/root/report_make/test_temp.txt"

with open(test_file_path, 'w') as f:
    f.write(test_content)

try:
    # 1. 第一次请求：带文件
    print("=== 测试 1: 带临时文件的报告生成 ===")
    files = {'files': ('test_temp.txt', open(test_file_path, 'rb'))}
    response1 = requests.post('http://localhost:8080/api/generate-report', 
                             files=files, 
                             data={'topic': '测试临时知识库'})
    
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"   ✅ 报告生成成功: {result1['status']}")
        print(f"   📄 报告字数: {result1['word_count']}")
        
        # 检查是否使用了临时知识库
        if 'Local Knowledge Base' in result1['content']:
            print("   ✅ 报告中包含本地知识库内容")
        else:
            print("   ⚠️  报告中未包含本地知识库内容")
    else:
        print(f"   ❌ 请求失败: {response1.status_code} {response1.text}")
    
    # 关闭文件
    files['files'][1].close()
    
    # 等待清理
    time.sleep(3)
    
    # 2. 检查文件是否存在
    print("\n=== 测试 2: 检查临时文件清理 ===")
    knowledge_dir = '/root/report_make/backend/database'
    if os.path.exists(knowledge_dir):
        knowledge_files = os.listdir(knowledge_dir)
        temp_files = [f for f in knowledge_files if f.startswith('upload_')]
        print(f"   📁 知识库目录中的临时文件数量: {len(temp_files)}")
        print(f"   🗑️  临时文件已被清理: {len(temp_files) == 0}")
    else:
        print(f"   ⚠️  知识库目录不存在: {knowledge_dir}")
    
    # 3. 第二次请求：不带文件
    print("\n=== 测试 3: 不带文件的报告生成 ===")
    response2 = requests.post('http://localhost:8080/api/generate-report',
                             data={'topic': '测试知识库清理'})
    
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"   ✅ 报告生成成功: {result2['status']}")
        
        # 检查是否不再包含临时知识库
        if 'Local Knowledge Base' not in result2['content']:
            print("   ✅ 报告中不再包含本地知识库内容")
        else:
            print("   ⚠️  报告中仍然包含本地知识库内容")
    else:
        print(f"   ❌ 请求失败: {response2.status_code} {response2.text}")
    
finally:
    # 清理测试文件
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
        print(f"\n📝 已清理测试文件")
    
print("\n=== 测试完成 ===")
