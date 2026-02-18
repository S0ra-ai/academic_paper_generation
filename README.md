# Academic Paper Generation System


- [English](#academic-paper-generation-system)
- [中文 (简体)](#学术论文报告生成系统)

---

## Academic Paper Generation System

A complete academic paper report generation system, including backend API services and frontend web application, supporting AI-based automatic academic paper report generation.

### Project Introduction

This project aims to help researchers quickly generate high-quality academic papers or reports by integrating multiple academic literature retrieval sources and large language models (LLMs), combined with Retrieval-Augmented Generation (RAG) technology, to realize the full-process automation from literature collection to report writing.

- **Advanced Academic Literature Search**: Integrates multiple authoritative academic platforms such as Crossref, OpenAlex, ArXiv, and Semantic Scholar, supporting concurrent retrieval and intelligent filtering
- **Retrieval-Augmented Generation (RAG)**: Integrates academic literature retrieval results with local knowledge base, significantly improving the accuracy and relevance of report content
- **Intelligent Report Generation**: LLM-based report content generation and organization, supporting multiple languages
- **Local Knowledge Base Management**: Supports loading, automatic segmentation, and vector indexing of PDF, DOCX and other format documents
- **Custom Template Functionality**: Supports users to create and use custom report templates, flexibly controlling report structure and content
- **User-Friendly Web Interface**: Intuitive report generation and management interface
- **Docker Containerized Deployment**: Simplifies deployment and environment configuration

### Technology Stack

#### Backend Core Technology
- **Python 3.9+**: Main development language
- **Flask 2.0+**: Web framework, providing RESTful API
- **Transformers**: Local Embedding model, supporting document vectorization
- **LangChain**: RAG technology implementation, integrating retrieval results with knowledge base
- **OpenRouter API**: Large language model service, supporting intelligent content generation
- **Multi-threaded Concurrency**: Implements efficient parallel retrieval of academic literature
- **Vector Database**: Supports efficient storage and retrieval of local knowledge base

#### Frontend Technology
- **Vue.js 3**: Modern frontend framework
- **Vite**: Fast build tool
- **Tailwind CSS**: Responsive UI design

#### Deployment Technology
- **Docker**: Containerized deployment
- **Docker Compose**: Multi-service coordination management

### Project Structure

```
academic_paper_generation/
├── backend/           # Backend API service
│   ├── app/           # Application core code
│   │   ├── api/       # API routes
│   │   ├── services/  # Business logic services
│   │   └── app.py     # Flask application main file
│   ├── config/        # Configuration files
│   ├── database/      # Database files
│   ├── requirements.txt  # Python dependencies
│   └── README.md      # Backend service documentation
├── frontend/          # Frontend web application
│   ├── src/           # Source code
│   ├── public/        # Static resources
│   ├── package.json   # Frontend dependencies
│   └── vite.config.js # Vite configuration
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile.backend # Backend Dockerfile
├── Dockerfile.frontend # Frontend Dockerfile
└── README.md          # Project documentation
```

### Quick Start

#### Method 1: Using Docker Compose (Recommended)

1. **Clone the repository**

```bash
git clone https://github.com/S0ra-ai/academic_paper_generation.git
cd academic_paper_generation
```

2. **Configure environment variables**

Copy and edit the backend environment variable file:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env file, fill in API keys and other configurations
```

3. **Start services**

```bash
docker-compose up -d
```

Services will start at the following addresses:
- Frontend application: http://localhost:3000
- Backend API: http://localhost:5000

#### Method 2: Local Development Environment

##### 1. Start backend service

```bash
cd backend
pip install -r requirements.txt
# Configure .env file
python app/app.py
```

##### 2. Start frontend application

```bash
cd frontend
npm install
npm run dev
```

### Main Features

#### 1. RAG-Driven Academic Report Generation

- **Intelligent Literature Retrieval**: Input research topic, the system automatically retrieves relevant literature from multiple academic platforms
- **Knowledge Integration**: Deeply integrates academic literature retrieval results with local knowledge base content
- **Structured Reports**: Generates logically clear, content-rich structured reports based on integrated knowledge
- **Multi-language Support**: Supports report generation in multiple languages including Chinese and English
- **Content Accuracy**: Significantly improves the accuracy and academic relevance of generated content through RAG technology

#### 2. Advanced Academic Literature Search System

- **Multi-source Integration**: Simultaneously integrates authoritative academic platforms such as Crossref, OpenAlex, ArXiv, and Semantic Scholar
- **Concurrent Retrieval**: Multi-threaded parallel retrieval, greatly improving search efficiency
- **Intelligent Processing**: Automatic filtering, sorting, and deduplication of retrieval results
- **Comprehensive Coverage**: Ensures access to the most relevant and latest academic research results
- **Standardized Processing**: Unifies literature formats from different platforms for subsequent analysis and use

#### 3. Intelligent Local Knowledge Base Management

- **Multi-format Support**: Compatible with multiple document formats such as PDF and DOCX
- **Automatic Processing**: Intelligent document segmentation, text extraction, and vector indexing
- **Efficient Retrieval**: Semantic-based fast document content retrieval
- **Continuous Optimization**: Supports dynamic updating and expansion of knowledge base
- **Secure Storage**: Local storage ensures data privacy and security

#### 4. Complete Report Management Functionality

- **History Records**: View and manage all historically generated reports
- **Content Preview**: Online preview of report content
- **Convenient Download**: Support for report export and saving

#### 5. Custom Template Functionality

- **Template Creation**: Users can create personalized report templates according to their needs
- **Template Management**: Support for saving, editing, and deleting templates
- **Flexible Configuration**: Customizable report structure, chapter layout, and content requirements
- **Template Application**: Select to use custom templates during report generation
- **Structure Control**: Precisely control the logical structure and content organization of generated reports through templates
- **Reusability**: Created templates can be reused, improving the consistency and efficiency of report generation

### API Documentation

Backend API service provides the following main endpoints:

#### Health Check
- **GET /health** - Check API service status

#### Report Generation
- **POST /api/generate-report** - Generate academic report
  - Request body: `{"query": "Research topic", "limit": 6, "language": "zh"}`
  - Response: Generated report content

#### Report Management
- **GET /api/reports** - Get report list
- **GET /api/reports/{id}** - Get report details
- **DELETE /api/reports/{id}** - Delete report

#### Template Management
- **GET /api/get-templates** - Get template list
- **POST /api/upload-template** - Upload new template

Detailed API documentation can be found in [Backend Service Documentation](backend/README.md).

### Configuration Instructions

#### Backend Configuration

Main configuration items (located in `backend/.env`):

- `OPENROUTER_API_KEY` - OpenRouter API key
- `SERPAPI_KEY` - SerpAPI key (for certain retrieval functions)
- `ACADEMIC_EMAIL` - Academic email (for API request identification)
- `LLM_MODEL_NAME` - LLM model name to use
- `KNOWLEDGE_DIR` - Local knowledge base directory
- `SAVE_DIR` - Report save directory

#### Frontend Configuration

Frontend configuration is mainly managed through environment variables and configuration files:

- `VITE_API_BASE_URL` - Backend API base URL

### Deployment Instructions

#### Docker Deployment

The project provides complete Docker configuration, supporting one-click deployment:

```bash
# Build and start all services
docker-compose up -d --build

# Build and start backend service separately
docker-compose up -d --build backend

# Build and start frontend service separately
docker-compose up -d --build frontend

# View service status
docker-compose ps

# Stop backend service
docker-compose stop backend

# Stop frontend service
docker-compose stop frontend
```

#### Production Environment Deployment

1. Ensure to modify environment variable configurations in `docker-compose.yml`
2. Configure appropriate network and port mappings
3. Consider using HTTPS certificates to protect services
4. Regularly back up database and report files

### Development Guide

#### Backend Development

1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `python -m pytest`
3. Start development server: `python backend\main.py`

#### Frontend Development

1. Install dependencies: `npm install`
2. Start development server: `npm run dev`
3. Build production version: `npm run build`

### Notes

1. **API Keys**: Ensure correct configuration of OpenRouter API and SerpAPI keys, otherwise report generation functionality will not work
2. **Resource Requirements**: Running local Embedding models requires certain memory resources (recommended at least 8GB RAM)
3. **Network Connection**: Academic literature retrieval requires a stable network connection

### Disclaimer

This project is for learning reference only, aiming to help researchers understand the automated process of academic report generation and related technical implementations.

- **Usage Responsibility**: All impacts resulting from the use of this project are unrelated to the project authors
- **Compliance**: Users should ensure compliance with relevant laws, regulations, and academic norms
- **API Usage**: When using third-party APIs, users should comply with the terms of service of the corresponding service providers

---

## 学术论文报告生成系统

一个完整的学术论文报告生成系统，包含后端API服务和前端Web应用，支持基于人工智能的学术论文报告自动生成。

### 项目简介

本项目旨在帮助研究人员快速生成高质量的学术论文或报告，通过集成多种学术文献检索源和大语言模型（LLM），结合检索增强生成（RAG）技术，实现从文献收集到报告撰写的全流程自动化。

- **高级学术文献搜索**：集成Crossref、OpenAlex、ArXiv、Semantic Scholar等多个权威学术平台，支持并发检索和智能过滤
- **检索增强生成（RAG）**：融合学术文献检索结果与本地知识库，显著提升报告内容的准确性和相关性
- **智能报告生成**：基于LLM的报告内容生成和组织，支持多种语言
- **本地知识库管理**：支持PDF、DOCX等格式文档的加载、自动分割和向量索引
- **自定义模板功能**：支持用户创建和使用自定义报告模板，灵活控制报告结构和内容
- **用户友好的Web界面**：直观的报告生成和管理界面
- **Docker容器化部署**：简化部署和环境配置

### 技术栈

#### 后端核心技术
- **Python 3.9+**：主要开发语言
- **Flask 2.0+**：Web框架，提供RESTful API
- **Transformers**：本地Embedding模型，支持文档向量化
- **LangChain**：RAG技术实现，融合检索结果与知识库
- **OpenRouter API**：大语言模型服务，支持智能内容生成
- **多线程并发**：实现高效的学术文献并行检索
- **向量数据库**：支持本地知识库的高效存储和检索

#### 前端技术
- **Vue.js 3**：现代前端框架
- **Vite**：快速构建工具
- **Tailwind CSS**：响应式UI设计

#### 部署技术
- **Docker**：容器化部署
- **Docker Compose**：多服务协调管理

### 项目结构

```
acacademic_paper_generation/
├── backend/           # 后端API服务
│   ├── app/           # 应用核心代码
│   │   ├── api/       # API路由
│   │   ├── services/  # 业务逻辑服务
│   │   └── app.py     # Flask应用主文件
│   ├── config/        # 配置文件
│   ├── database/      # 数据库文件
│   ├── requirements.txt  # Python依赖
│   └── README.md      # 后端服务说明
├── frontend/          # 前端Web应用
│   ├── src/           # 源代码
│   ├── public/        # 静态资源
│   ├── package.json   # 前端依赖
│   └── vite.config.js # Vite配置
├── docker-compose.yml # Docker Compose配置
├── Dockerfile.backend # 后端Dockerfile
├── Dockerfile.frontend # 前端Dockerfile
└── README.md          # 项目说明文档
```

### 快速开始

#### 方法一：使用Docker Compose（推荐）

1. **克隆仓库**

```bash
git clone https://github.com/S0ra-ai/academic_paper_generation.git
cd academic_paper_generation
```

2. **配置环境变量**

复制并编辑后端环境变量文件：

```bash
cp backend/.env.example backend/.env
# 编辑backend/.env文件，填写API密钥等配置
```

3. **启动服务**

```bash
docker-compose up -d
```

服务将在以下地址启动：
- 前端应用：http://localhost:3000
- 后端API：http://localhost:5000

#### 方法二：本地开发环境

##### 1. 启动后端服务

```bash
cd backend
pip install -r requirements.txt
# 配置.env文件
python app/app.py
```

##### 2. 启动前端应用

```bash
cd frontend
npm install
npm run dev
```

### 主要功能

#### 1. 检索增强生成（RAG）驱动的学术报告生成

- **智能文献检索**：输入研究主题，系统自动从多个学术平台检索相关文献
- **知识融合**：将学术文献检索结果与本地知识库内容深度融合
- **结构化报告**：基于融合知识生成逻辑清晰、内容丰富的结构化报告
- **多语言支持**：支持中英文等多种语言的报告生成
- **内容准确性**：通过RAG技术显著提升生成内容的准确性和学术相关性

#### 2. 高级学术文献搜索系统

- **多源集成**：同时整合Crossref、OpenAlex、ArXiv、Semantic Scholar等权威学术平台
- **并发检索**：多线程并行检索，大幅提高搜索效率
- **智能处理**：自动过滤、排序和去重检索结果
- **全面覆盖**：确保获取最相关、最新的学术研究成果
- **标准化处理**：统一不同平台的文献格式，便于后续分析和使用

#### 3. 智能本地知识库管理

- **多格式支持**：兼容PDF、DOCX等多种文档格式
- **自动处理**：智能文档分割、文本提取和向量索引
- **高效检索**：基于语义的快速文档内容检索
- **持续优化**：支持知识库的动态更新和扩展
- **安全存储**：本地存储确保数据隐私和安全

#### 4. 完整报告管理功能

- **历史记录**：查看和管理所有历史生成的报告
- **内容预览**：在线预览报告内容
- **便捷下载**：支持报告的导出和保存

#### 5. 自定义模板功能

- **模板创建**：用户可根据需求创建个性化报告模板
- **模板管理**：支持模板的保存、编辑和删除
- **灵活配置**：可自定义报告结构、章节布局和内容要求
- **模板应用**：在报告生成时选择使用自定义模板
- **结构控制**：通过模板精确控制生成报告的逻辑结构和内容组织
- **复用性**：创建的模板可重复使用，提高报告生成的一致性和效率

### API文档

后端API服务提供以下主要端点：

#### 健康检查
- **GET /health** - 检查API服务状态

#### 报告生成
- **POST /api/generate-report** - 生成学术报告
  - 请求体：`{"query": "研究主题", "limit": 6, "language": "zh"}`
  - 响应：生成的报告内容

#### 报告管理
- **GET /api/reports** - 获取报告列表
- **GET /api/reports/{id}** - 获取报告详情
- **DELETE /api/reports/{id}** - 删除报告

#### 模板管理
- **GET /api/get-templates** - 获取模板列表
- **POST /api/upload-template** - 上传新模板

详细API文档请参考 [后端服务说明](backend/README.md)。

### 配置说明

#### 后端配置

主要配置项（位于`backend/.env`）：

- `OPENROUTER_API_KEY` - OpenRouter API密钥
- `SERPAPI_KEY` - SerpAPI密钥（用于某些检索功能）
- `ACADEMIC_EMAIL` - 学术邮箱（用于API请求标识）
- `LLM_MODEL_NAME` - 使用的LLM模型名称
- `KNOWLEDGE_DIR` - 本地知识库目录
- `SAVE_DIR` - 报告保存目录

#### 前端配置

前端配置主要通过环境变量和配置文件管理：

- `VITE_API_BASE_URL` - 后端API基础URL

### 部署说明

#### Docker部署

项目提供了完整的Docker配置，支持一键部署：

```bash
# 构建并启动所有服务
docker-compose up -d --build

# 单独构建并启动后端服务
docker-compose up -d --build backend

# 单独构建并启动前端服务
docker-compose up -d --build frontend

# 查看服务状态
docker-compose ps

# 停止后端服务
docker-compose stop backend

# 停止前端服务
docker-compose stop frontend
```

#### 生产环境部署

1. 确保修改`docker-compose.yml`中的环境变量配置
2. 配置适当的网络和端口映射
3. 考虑使用HTTPS证书保护服务
4. 定期备份数据库和报告文件

### 开发指南

#### 后端开发

1. 安装依赖：`pip install -r requirements.txt`
2. 运行测试：`python -m pytest`
3. 启动开发服务器：`python backend\main.py`

#### 前端开发

1. 安装依赖：`npm install`
2. 启动开发服务器：`npm run dev`
3. 构建生产版本：`npm run build`

### 注意事项

1. **API密钥**：确保正确配置OpenRouter API与SERPAPI密钥，否则报告生成功能将无法使用
2. **资源需求**：运行本地Embedding模型需要一定的内存资源（建议至少8GB RAM）
3. **网络连接**：学术文献检索需要稳定的网络连接

### 免责声明

本项目仅供学习参考使用，旨在帮助研究人员了解学术报告生成的自动化流程和相关技术实现。

- **使用责任**：使用本项目产生的一切影响与项目作者无关
- **合规性**：使用者应确保遵守相关法律法规和学术规范
- **API使用**：使用第三方API时应遵守相应服务提供商的使用条款