import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# 加载配置
from config.config import Config

# 导入数据库模型
from app.models import db

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

# 创建Flask应用
app = Flask(__name__)

# 加载配置
app.config.from_object(Config)

# 初始化数据库
with app.app_context():
    db.init_app(app)

# 启用CORS，允许跨域请求，特别配置以支持文件上传
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Origin", "Content-Type", "Accept", "Authorization", "X-Requested-With"],
    "supports_credentials": True
}})

# 导入并注册API蓝图
from app.api.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# 配置环境变量 - 在应用启动时直接配置
def configure_environment():
    """配置环境变量"""
    # 环境变量优化 - 设置为离线模式
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'  # 保留镜像地址，但不实际下载
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    os.environ['SENTENCE_TRANSFORMERS_HOME'] = './.cache/sentence_transformers'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'  # 强制使用离线模式
    os.environ['HF_HUB_OFFLINE'] = '1'  # HuggingFace Hub离线模式

# 直接调用环境配置函数
configure_environment()

# 健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    """应用健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'message': 'Academic Report API is running'
    }), 200

# 根路径重定向到前端应用
@app.route('/', methods=['GET'])
def root_redirect():
    """根路径重定向到前端应用"""
    from flask import redirect
    return redirect('http://43.153.41.145:4173/', code=302)

if __name__ == '__main__':
    # 启动Flask应用
    app.run(host='0.0.0.0', port=8080, debug=False)