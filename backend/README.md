# 学术报告生成API

一个基于Flask的后端API服务，专注于检索增强生成（RAG）驱动的学术报告生成，集成多种学术文献搜索源，提供RESTful API接口供前端调用。

## 项目结构

```
backend/
├── app/
│   ├── api/               # API路由模块
│   │   ├── __init__.py
│   │   └── routes.py      # API端点定义
│   ├── services/          # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── llm_service.py         # LLM服务：翻译、推理和写作
│   │   ├── search_service.py      # 搜索服务：学术文献检索
│   │   ├── local_doc_service.py   # 本地文档服务：知识库管理
│   │   └── report_generator.py    # 报告生成服务：协调各模块生成报告
│   ├── utils/             # 工具函数
│   │   └── __init__.py
│   └── app.py             # Flask应用主文件
├── config/                # 配置文件
│   └── config.py          # 应用配置类
├── .env.example           # 环境变量示例
├── requirements.txt       # Python依赖列表
└── README.md              # 项目说明文档
```

## 功能模块

1. **LLM服务** (`llm_service.py`)
   - 负责与OpenRouter API通信
   - 提供翻译、推理和写作功能
   - 支持重试机制，确保请求可靠

2. **搜索服务** (`search_service.py`)
   - 提供多源学术文献检索功能
   - 支持Crossref、OpenAlex、ArXiv、Semantic Scholar等平台
   - 实现并发检索，提高效率

3. **本地文档服务** (`local_doc_service.py`)
   - 管理本地知识库
   - 支持文档加载、分割和向量索引
   - 提供本地文档检索功能

4. **报告生成服务** (`report_generator.py`)
   - 协调各服务模块
   - 实现报告生成的完整流程
   - 集成本地RAG功能

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制`.env.example`文件并命名为`.env`，然后填写相应的配置信息：

```bash
cp .env.example .env
# 编辑.env文件，填写API密钥等配置
```

### 3. 启动服务

```bash
cd backend
python app/app.py
```

服务将在`http://localhost:5000`启动。

## API端点

### 健康检查

```
GET /health
```

检查API服务是否正常运行。

### 生成报告

```
POST /api/generate-report
```

请求体：
```json
{
  "query": "人工智能在医疗领域的应用",
  "limit": 6,  // 可选，每个数据源检索的文献数量
  "language": "zh"  // 可选，生成报告的语言
}
```

响应：
```json
{
  "status": "success",
  "data": {
    "report": "生成的学术报告内容...",
    "query": "人工智能在医疗领域的应用"
  },
  "message": "报告生成成功"
}
```

## 配置说明

- `OPENROUTER_API_KEY`: OpenRouter API密钥
- `SERPAPI_KEY`: SerpAPI密钥
- `ACADEMIC_EMAIL`: 学术邮箱（用于OpenAlex等平台的礼貌请求）
- `LLM_MODEL_NAME`: 使用的LLM模型名称
- `LLM_TEMPERATURE`: LLM生成的温度参数
- `LLM_MAX_TOKENS`: LLM生成的最大token数
- `LLM_TIMEOUT`: LLM请求超时时间
- `KNOWLEDGE_DIR`: 本地知识库目录
- `SAVE_DIR`: 报告保存目录
- `SEARCH_LIMIT`: 每个数据源检索的文献数量

## 注意事项

1. 确保已安装所有依赖包
2. 配置正确的API密钥
3. 本地知识库需要手动创建并放入相关文档
4. 首次启动时，服务会尝试加载本地Embedding模型

## 开发说明

- 该服务使用Flask框架构建
- 采用模块化设计，各功能模块职责明确
- 支持CORS，可与前端应用无缝集成
- 实现了完善的错误处理和日志记录

## 免责声明

本项目仅供学习参考使用，旨在帮助研究人员了解学术报告生成的自动化流程和相关技术实现。

- **使用责任**：使用本项目产生的一切影响与项目作者无关
- **合规性**：使用者应确保遵守相关法律法规和学术规范
- **内容准确性**：系统生成的报告内容仅供参考，使用者应自行核实信息的准确性
- **API使用**：使用第三方API时应遵守相应服务提供商的使用条款


