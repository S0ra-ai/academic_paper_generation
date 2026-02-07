import requests
import os
import time
import tempfile

# 创建临时测试文件
with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as f:
    f.write("这是测试临时知识库的内容。")
    temp_file_path = f.name
    temp_file_name = os.path.basename(temp_file_path)

# 测试文件上传和报告生成
def test_temporary_knowledge():
    print("=== 测试临时知识库功能 ===")
    
    # 准备测试数据
    url = 'http://localhost:8080/api/generate-report'
    files = {'files': (temp_file_name, open(temp_file_path, 'rb'), 'text/plain')}
    data = {'topic': '测试临时知识库'}
    
    try:
        # 第一次请求：使用临时知识库生成报告
        print("\n1. 发送第一次请求（带临时文件）...")
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   成功: {result['status']}")
            print(f"   报告内容包含临时知识库: {'Local Knowledge Base' in result['content']}")
        else:
            print(f"   失败: {response.status_code}, {response.text}")
        
        # 关闭文件
        for file_tuple in files.values():
            file_tuple[1].close()
        
        # 等待清理完成
        time.sleep(2)
        
        # 检查临时文件是否被删除
        print(f"\n2. 检查临时文件是否被删除: {not os.path.exists(temp_file_path)}")
        
        # 第二次请求：不使用临时知识库，验证知识库已被清理
        print("\n3. 发送第二次请求（不带文件）...")
        response2 = requests.post(url, data={'topic': '测试知识库清理'})
        
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"   成功: {result2['status']}")
            print(f"   报告内容不包含临时知识库: {'Local Knowledge Base' not in result2['content']}")
        else:
            print(f"   失败: {response2.status_code}, {response2.text}")
        
        print("\n=== 测试完成 ===")
        return True
        
    except Exception as e:
        print(f"测试出错: {e}")
        return False
    finally:
        # 清理测试文件
        if os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass

if __name__ == "__main__":
    test_temporary_knowledge()