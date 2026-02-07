from flask import Blueprint, request, jsonify
import logging
import os
import threading
from werkzeug.utils import secure_filename

from app.services.report_generator import ReportGenerator
from app.services.local_doc_service import LocalDocManager
from config.config import Config

# 创建API蓝图
api_bp = Blueprint('api', __name__)

# 初始化报告生成器
report_generator = ReportGenerator()

@api_bp.route('/generate-report', methods=['POST'])
def generate_report():
    """
    生成学术报告的API端点
    ---
    parameters:
      - name: topic
        in: body
        required: true
        schema:
          type: object
          properties:
            topic: {
              type: string,
              description: '研究主题'
            }
    responses:
      200:
        description: 报告生成成功
        schema:
          type: object
          properties:
            status: {
              type: string,
              description: '生成状态'
            }
            filename: {
              type: string,
              description: '生成的文件名'
            }
            filepath: {
              type: string,
              description: '文件路径'
            }
            content: {
              type: string,
              description: '报告内容'
            }
            word_count: {
              type: integer,
              description: '报告字数'
            }
      400:
        description: 请求参数错误
      500:
        description: 服务器内部错误
    """
    try:
        # 打印请求信息以调试
        logging.info(f"📥 请求类型: {request.content_type}")
        logging.info(f"📥 请求方法: {request.method}")
        logging.info(f"📥 请求表单: {list(request.form.items())}")
        logging.info(f"📥 请求文件: {list(request.files.keys())}")
        
        # 统一处理topic获取
        topic = request.form.get('topic', '')
        if not topic and request.is_json:
            data = request.get_json()
            topic = data.get('topic', '')
        topic = topic.strip()
        
        # 处理模板参数
        template = request.form.get('template', '')
        if not template and request.is_json:
            data = request.get_json()
            template = data.get('template', '')
        template = template.strip()
        
        logging.info(f"📥 获取到的topic: {topic}")
        
        # 初始化变量
        uploaded_files = []
        temp_files = []
        local_doc_manager = LocalDocManager()
        
        # 处理文件上传
        if 'files' in request.files:
            files = request.files.getlist('files')
            logging.info(f"📥 接收到 {len(files)} 个文件")
            
            # 确保知识库目录存在
            os.makedirs(Config.KNOWLEDGE_DIR, exist_ok=True)
            
            # 保存上传的文件
            import time
            for file in files:
                if file.filename:
                    # 保持原始文件名，只移除最危险的字符（路径分隔符、控制字符等）
                    import re
                    filename = file.filename
                    # 移除路径分隔符和空字符
                    filename = re.sub(r'[\/\x00]', '_', filename)
                    # 移除控制字符
                    filename = re.sub(r'[\x01-\x1f\x7f]', '', filename)
                    # 确保文件名不为空
                    filename = filename.strip()
                    if not filename:
                        filename = f"upload_{int(time.time())}"
                    
                    # 处理只有扩展名的情况，如'docx'，添加时间戳前缀
                    _, ext = os.path.splitext(filename)
                    if not ext and len(filename) <= 5:
                        # 如果没有点号且长度较短，视为只有扩展名
                        timestamp = int(time.time())
                        filename = f"upload_{timestamp}.{filename}"
                    
                    file_path = os.path.join(Config.KNOWLEDGE_DIR, filename)
                    
                    # 保存文件
                    file.save(file_path)
                    uploaded_files.append(filename)
                    logging.info(f"✅ 文件已保存: {file_path}")
                    
                    # 记录临时文件路径
                    temp_files.append(file_path)
            
            # 如果有文件上传，更新知识库索引（临时模式）
            if uploaded_files:
                logging.info(f"🔄 更新知识库索引（临时模式），新增文件: {uploaded_files}")
                # 合并build_index返回的temp_files列表，包含转换后的Word文件路径
                index_temp_files = local_doc_manager.build_index(uploaded_files, use_temp_storage=True)
                if index_temp_files:
                    temp_files.extend(index_temp_files)
        
        if not topic:
            return jsonify({
                'status': 'error',
                'message': '研究主题不能为空'
            }), 400
        
        # 生成报告，传入临时知识库实例和模板参数
        result = report_generator.generate_report(topic, local_rag=local_doc_manager, template=template)
        
        # 清理临时文件和知识库
        try:
            # 清除向量数据库
            local_doc_manager.vector_db = None
            logging.info("📌 已清除向量数据库，知识库将在下一次构建时重新创建")
            
            # 删除临时文件
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logging.info(f"🗑️  已删除临时文件: {temp_file}")
        except Exception as e:
            logging.error(f"⚠️  清理资源时出错: {e}")
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logging.error(f"API 错误: {e}")
        return jsonify({
            'status': 'error',
            'message': f'服务器内部错误: {str(e)}'
        }), 500


@api_bp.route('/upload-template', methods=['POST'])
def upload_template():
    """
    上传研究报告模板的API端点
    ---
    parameters:
      - name: template
        in: formData
        type: file
        required: true
        description: 研究报告模板文件
    responses:
      200:
        description: 模板上传成功
        schema:
          type: object
          properties:
            status: { type: string, description: '上传状态' }
            message: { type: string, description: '上传结果消息' }
            filename: { type: string, description: '保存的模板文件名' }
      400:
        description: 请求参数错误
      500:
        description: 服务器内部错误
    """
    try:
        # 检查是否有文件上传
        if 'template' not in request.files:
            return jsonify({
                'status': 'error',
                'message': '未收到模板文件'
            }), 400
        
        file = request.files['template']
        
        # 检查文件是否有文件名
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': '未选择模板文件'
            }), 400
        
        # 确保模板目录存在
        os.makedirs(Config.TEMPLATES_DIR, exist_ok=True)
        
        # 保存文件，保留原始文件名
        filename = file.filename
        import re
        # 移除路径分隔符和空字符
        filename = re.sub(r'[\/\x00]', '_', filename)
        # 移除控制字符
        filename = re.sub(r'[\x01-\x1f\x7f]', '', filename)
        filename = filename.strip()
        
        file_path = os.path.join(Config.TEMPLATES_DIR, filename)
        file.save(file_path)
        
        logging.info(f"✅ 模板文件已保存: {file_path}")
        
        return jsonify({
            'status': 'success',
            'message': '模板上传成功',
            'filename': filename
        }), 200
        
    except Exception as e:
        logging.error(f"❌ 模板上传失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'服务器内部错误: {str(e)}'
        }), 500


@api_bp.route('/get-templates', methods=['GET'])
def get_templates():
    """
    获取已上传模板列表的API端点
    ---
    responses:
      200:
        description: 模板列表获取成功
        schema:
          type: object
          properties:
            status: { type: string, description: '请求状态' }
            templates: { 
              type: array,
              items: { type: string },
              description: '已上传的模板文件名列表'
            }
      500:
        description: 服务器内部错误
    """
    try:
        # 确保模板目录存在
        os.makedirs(Config.TEMPLATES_DIR, exist_ok=True)
        
        # 获取模板文件列表
        templates = []
        for file in os.listdir(Config.TEMPLATES_DIR):
            file_path = os.path.join(Config.TEMPLATES_DIR, file)
            if os.path.isfile(file_path):
                templates.append(file)
        
        logging.info(f"✅ 获取模板列表成功，共 {len(templates)} 个模板")
        
        return jsonify({
            'status': 'success',
            'templates': templates
        }), 200
        
    except Exception as e:
        logging.error(f"❌ 获取模板列表失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'服务器内部错误: {str(e)}'
        }), 500