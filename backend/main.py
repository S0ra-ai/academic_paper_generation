import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并启动Flask应用
from app.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)