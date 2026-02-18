import os
import time
import json
import logging
from typing import Dict, List
from datetime import datetime

from app.services.llm_service import LLMService
from config.config import Config

class CodeAnalyzer:
    def __init__(self):
        self.llm = LLMService()
        self.code_dir = os.path.join(os.path.abspath(Config.KNOWLEDGE_DIR), 'code')
        os.makedirs(self.code_dir, exist_ok=True)
        logging.info("✅ 代码分析器初始化完成")

    def analyze_code(self, file_path: str) -> Dict:
        """
        分析单个代码文件
        """
        try:
            # 获取文件扩展名
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            
            # 根据文件类型进行分析
            if ext == '.java':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                return self._analyze_java_file(file_path, content)
            elif ext == '.py':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                return self._analyze_python_file(file_path, content)
            else:
                # 对于本地参考文献文件，返回基本信息
                return {
                    'status': 'success',
                    'file_type': 'reference',
                    'file_name': os.path.basename(file_path),
                    'file_size': os.path.getsize(file_path),
                    'message': '本地参考文献文件'
                }
        except Exception as e:
            logging.error(f"❌ 分析文件失败: {file_path}, 错误: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def _analyze_java_file(self, file_path: str, content: str) -> Dict:
        """
        分析Java文件
        """
        import re
        
        # 提取类名
        class_match = re.search(r'class\s+(\w+)', content)
        class_name = class_match.group(1) if class_match else os.path.basename(file_path)
        
        # 提取方法名
        methods = re.findall(r'(public|private|protected)\s+\w+\s+(\w+)\s*\(', content)
        method_names = [m[1] for m in methods]
        
        # 提取导入语句
        imports = re.findall(r'import\s+([\w\.]+);', content)
        
        # 提取注释
        comments = re.findall(r'(/\*[\s\S]*?\*/|//.*$)', content, re.MULTILINE)
        
        return {
            'status': 'success',
            'file_type': 'java',
            'file_name': os.path.basename(file_path),
            'class_name': class_name,
            'methods': method_names,
            'imports': imports,
            'comment_count': len(comments),
            'lines_of_code': len(content.split('\n')),
            'content': content[:2000]  # 只保留前2000个字符
        }

    def _analyze_python_file(self, file_path: str, content: str) -> Dict:
        """
        分析Python文件
        """
        import re
        
        # 提取函数名
        functions = re.findall(r'def\s+(\w+)\s*\(', content)
        
        # 提取类名
        classes = re.findall(r'class\s+(\w+)', content)
        
        # 提取导入语句
        imports = re.findall(r'import\s+([\w\.]+)', content)
        from_imports = re.findall(r'from\s+([\w\.]+)\s+import', content)
        imports.extend(from_imports)
        
        # 提取注释
        comments = re.findall(r'("""[\s\S]*?"""|#.*$)', content, re.MULTILINE)
        
        return {
            'status': 'success',
            'file_type': 'python',
            'file_name': os.path.basename(file_path),
            'classes': classes,
            'functions': functions,
            'imports': imports,
            'comment_count': len(comments),
            'lines_of_code': len(content.split('\n')),
            'content': content[:2000]  # 只保留前2000个字符
        }

    def analyze_project(self, file_names: List[str]) -> Dict:
        """
        分析整个代码项目
        """
        try:
            project_analysis = {
                'total_files': len(file_names),
                'java_files': [],
                'python_files': [],
                'reference_files': [],
                'other_files': [],
                'total_lines_of_code': 0,
                'total_comments': 0,
                'total_reference_files_size': 0
            }
            
            for file_name in file_names:
                file_path = os.path.join(self.code_dir, file_name)
                analysis = self.analyze_code(file_path)
                
                if analysis['status'] == 'success':
                    if analysis['file_type'] == 'java':
                        project_analysis['java_files'].append(analysis)
                    elif analysis['file_type'] == 'python':
                        project_analysis['python_files'].append(analysis)
                    elif analysis['file_type'] == 'reference':
                        project_analysis['reference_files'].append(analysis)
                        # 更新本地参考文献文件大小
                        if 'file_size' in analysis:
                            project_analysis['total_reference_files_size'] += analysis['file_size']
                    else:
                        project_analysis['other_files'].append({
                            'file_name': file_name,
                            'message': '不支持的文件类型'
                        })
                    
                    # 更新统计信息
                    if 'lines_of_code' in analysis:
                        project_analysis['total_lines_of_code'] += analysis['lines_of_code']
                    if 'comment_count' in analysis:
                        project_analysis['total_comments'] += analysis['comment_count']
                else:
                    project_analysis['other_files'].append({
                        'file_name': file_name,
                        'message': analysis['message']
                    })
            
            return {
                'status': 'success',
                'analysis': project_analysis
            }
        except Exception as e:
            logging.error(f"❌ 分析项目失败: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def analyze_and_generate_report(self, project_name: str, file_names: List[str], template: str = "") -> Dict:
        """
        分析代码并生成报告
        """
        logging.info(f"💡 [阶段 1] 分析代码项目: {project_name}")
        logging.info(f"📁 分析文件数量: {len(file_names)}")
        
        try:
            # 分析项目
            analysis_result = self.analyze_project(file_names)
            
            if analysis_result['status'] != 'success':
                return analysis_result
            
            analysis = analysis_result['analysis']
            
            # 构建上下文
            context_str = f"# Project Analysis Report: {project_name}\n\n"
            context_str += f"## Project Overview\n"
            context_str += f"- Project Name: {project_name}\n"
            context_str += f"- Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            context_str += f"- Total Files: {analysis['total_files']}\n"
            context_str += f"- Java Files: {len(analysis['java_files'])}\n"
            context_str += f"- Python Files: {len(analysis['python_files'])}\n"
            context_str += f"- Local Reference Files: {len(analysis['reference_files'])}\n"
            context_str += f"- Other Files: {len(analysis['other_files'])}\n"
            context_str += f"- Total Lines of Code: {analysis['total_lines_of_code']}\n"
            context_str += f"- Total Comments: {analysis['total_comments']}\n"
            context_str += f"- Total Local Reference Files Size: {analysis['total_reference_files_size']} bytes\n\n"
            
            # 分析Java文件
            if analysis['java_files']:
                context_str += f"## Java File Analysis\n"
                for java_file in analysis['java_files']:
                    context_str += f"### {java_file['file_name']}\n"
                    context_str += f"- Class Name: {java_file['class_name']}\n"
                    context_str += f"- Number of Methods: {len(java_file['methods'])}\n"
                    context_str += f"- Number of Imports: {len(java_file['imports'])}\n"
                    context_str += f"- Number of Comments: {java_file['comment_count']}\n"
                    context_str += f"- Lines of Code: {java_file['lines_of_code']}\n"
                    if java_file['methods']:
                        context_str += f"- Method List: {', '.join(java_file['methods'])}\n"
                    if 'content' in java_file and java_file['content']:
                        context_str += f"- Key Content: {java_file['content'][:500]}...\n"  # 显示部分代码内容
                    context_str += "\n"
            
            # 分析Python文件
            if analysis['python_files']:
                context_str += f"## Python File Analysis\n"
                for python_file in analysis['python_files']:
                    context_str += f"### {python_file['file_name']}\n"
                    context_str += f"- Number of Classes: {len(python_file['classes'])}\n"
                    context_str += f"- Number of Functions: {len(python_file['functions'])}\n"
                    context_str += f"- Number of Imports: {len(python_file['imports'])}\n"
                    context_str += f"- Number of Comments: {python_file['comment_count']}\n"
                    context_str += f"- Lines of Code: {python_file['lines_of_code']}\n"
                    if python_file['classes']:
                        context_str += f"- Class List: {', '.join(python_file['classes'])}\n"
                    if python_file['functions']:
                        context_str += f"- Function List: {', '.join(python_file['functions'])}\n"
                    if 'content' in python_file and python_file['content']:
                        context_str += f"- Key Content: {python_file['content'][:500]}...\n"  # 显示部分代码内容
                    context_str += "\n"
            
            # 分析本地参考文献文件
            local_references = []
            if analysis['reference_files']:
                context_str += f"## Local Reference File Analysis\n"
                for i, reference_file in enumerate(analysis['reference_files'], start=21):  # 从21开始编号
                    context_str += f"### [{i}] {reference_file['file_name']}\n"
                    if 'file_size' in reference_file:
                        context_str += f"- File Size: {reference_file['file_size']} bytes\n"
                    context_str += f"- File Type: {reference_file['message']}\n"
                    context_str += f"- Citation Key: [{i}]\n"
                    context_str += "\n"
                    local_references.append((i, reference_file['file_name']))
            
            # 处理模板
            template_content = ""
            if template:
                template_path = os.path.join(Config.TEMPLATES_DIR, template)
                logging.info(f"📄 使用模板: {template_path}")
                
                if os.path.exists(template_path):
                    try:
                        # 根据文件扩展名选择不同的读取方式
                        file_ext = os.path.splitext(template_path)[1].lower()
                        if file_ext in ['.txt', '.md']:
                            # 读取纯文本文件
                            with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
                                template_text = f.readlines()
                        elif file_ext in ['.doc', '.docx']:
                            # 读取Word文档
                            try:
                                import docx
                                doc = docx.Document(template_path)
                                template_text = [paragraph.text for paragraph in doc.paragraphs]
                            except ImportError:
                                logging.error("⚠️  python-docx 未安装，无法读取Word文档模板")
                                template_text = []
                        else:
                            logging.error(f"⚠️  不支持的模板文件格式: {file_ext}")
                            template_text = []
                        
                        template_content = "\n".join(template_text)
                        logging.info(f"✅ 已读取模板文件: {template} (共 {len(template_content)} 字符)")
                    except Exception as e:
                        logging.error(f"⚠️  读取模板文件失败: {e}")
                        # 详细的错误信息，包括文件路径和实际存在的文件
                        import traceback
                        logging.error(f"🚨 模板读取详细错误: {traceback.format_exc()}")
                        # 列出Templates目录下的文件，帮助调试
                        templates_dir = os.path.dirname(template_path)
                        if os.path.exists(templates_dir):
                            files = os.listdir(templates_dir)
                            logging.info(f"📋 Templates目录下的文件: {files}")
                        else:
                            logging.error(f"📋 Templates目录不存在: {templates_dir}")
                        template_content = ""
                else:
                    logging.error(f"⚠️  模板文件不存在: {template_path}")
                    # 列出templates目录下的文件，帮助调试
                    templates_dir = os.path.dirname(template_path)
                    if os.path.exists(templates_dir):
                        files = os.listdir(templates_dir)
                        logging.info(f"📋 Templates目录下的文件: {files}")
                    else:
                        logging.error(f"📋 Templates目录不存在: {templates_dir}")
            
            # 构建报告生成提示
            # 构建带有模板的prompt
            template_requirement = ""
            if template_content:
                template_requirement = f"\n\n**Template Requirements:**\n**CRITICAL: You MUST strictly follow the structure, format, sections, and wording of the provided template. Your entire report MUST match the template's structure exactly.**\nIntegrate the research content into the template framework without modifying the template's structure. Here's the template content:\n\n{template_content}\n\n**IMPORTANT: Do not deviate from the template structure. Do not add any new sections. Do not remove any sections from the template. Use the template as a framework and fill in the content.**\n"
            
            # 构建本地参考文献引用信息
            local_references_info = ""
            if local_references:
                local_references_info = f"\n\n**Local References Information:**\nThe following local reference files are available for citation:\n"
                for ref_id, ref_name in local_references:
                    local_references_info += f"- [{ref_id}] [Local File] {ref_name} - Local Knowledge Base\n"
                local_references_info += "\nYou MUST cite these local reference files appropriately throughout the paper where relevant." 
            
            prompt = f"""You are a computer science professor tasked with generating a professional academic paper based on the following code project analysis results.

# Project Information
Project Name: {project_name}
Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Analysis Results
{context_str}

{local_references_info}

# Report Requirements
**CRITICAL INSTRUCTIONS: FAILURE TO FOLLOW THESE WILL RESULT IN AN UNSATISFACTORY PAPER**

1. **Format**: Academic Markdown format, using strict LaTeX mathematical formula format ($...$).
2. **Length**: **REQUIREMENT** - The paper must be at least 10,000 words in length. This is a mandatory requirement. If the paper is shorter than this, it will be rejected.
3. **Structure**: Must include the following sections:
   - Abstract
   - Introduction
   - System Architecture Design
   - Core Functionality Modules
   - Key Technical Implementations
   - Code Quality Analysis
   - Performance Evaluation
   - Conclusions and Future Work
   - References
4. **Language**: Write in Chinese, maintaining a professional academic tone.
5. **Code Analysis**: Based on the provided code analysis results, deeply analyze code structure, design patterns, algorithm implementations, etc.
6. **Technical Depth**: Demonstrate computer science technical depth, including but not limited to:
   - Software engineering practices
   - Design pattern applications
   - Algorithm complexity analysis
   - Code quality evaluation
   - Performance optimization recommendations
7. **Code Integration**:
   - The code must be directly integrated into the paper body where relevant
   - Use Markdown code block format with proper source file attribution
   - Extract code snippets entirely from the project repository without any modifications
   - Code should be analyzed and discussed in detail within the paper content
   - Do not list code files in the references section
8. **References and Citations**:
   - **MANDATORY CITATION REQUIREMENT**: Every argument, claim, or fact must be cited with appropriate references. You cannot make any statement without citing a source.
   - **Prioritize citing local knowledge base content** to increase its weight in the report
   - **Strict numbering requirement**: Use the original numbering from the context exactly as provided (e.g., if the context uses [5], only cite [5], do not change the numbering)
   - **Citation markers**:
     - **Local knowledge base resources**: Use numbering greater than 20 (e.g., [21], [22]) as provided in the Local References Information section
     - **Web search resources**: Use numbering from 1-20 (e.g., [1], [15])
   - **References Section**:
     - Must list all cited literature, **strictly in the original numbering order from the context**
     - **Clearly distinguish between local knowledge base and web search resources** using different sections or markers
     - **Format requirements**:
       - Local knowledge base resources: Use "[Local File]" prefix, format: [number] [Local File] filename - Local Knowledge Base
       - Web search resources: Use normal format, e.g.: [number] 作者. 标题. 来源 (年份). URL
     - **Critical matching requirement**: References list numbering must exactly match the citations in the text. Do not change numbering or order under any circumstances.
   - **Additional Notes**:
     - Uploaded code project files MUST be directly integrated into the paper body and analyzed in detail
     - Code files should NOT appear in the references section
     - Local reference files MUST be appropriately cited in the references section
     - Mainly cite academic literature and technical documentation

9. **Template Adherence**:
   - **ABSOLUTE REQUIREMENT**: You must strictly follow the structure, format, sections, and wording of the provided template. Your entire report must match the template's structure exactly.
   - **No deviations allowed**: Do not add any new sections, do not remove any sections, and do not modify the template's structure in any way.
   - **Integration requirement**: Integrate the research content into the template framework while preserving the template's original structure and formatting.

{template_requirement}

# Writing Process Instructions
1. **First, analyze the template**: Carefully read and understand the template structure, formatting, and requirements.
2. **Second, plan the paper**: Create a detailed outline that fills the template structure with content from the code analysis results, ensuring it will reach at least 10,000 words.
3. **Third, write with citations**: As you write each section, ensure every statement is properly cited using the required numbering system. Make sure to cite local reference files where relevant.
4. **Fourth, verify length**: After writing, check the word count to ensure it is at least 10,000 words in length.
5. **Fifth, review references**: Verify that all citations in the text have corresponding entries in the references section, and that numbering matches exactly.

Please generate a computer science paper report that meets all of the above requirements. This is a formal academic paper, and adherence to all guidelines is mandatory."""
            
            logging.info(f"✍️ [阶段 2] 生成代码分析报告中 (Context: {len(context_str)} chars)...")
            
            # 限制提示词长度，避免超过API限制
            max_prompt_length = 100000
            if len(prompt) > max_prompt_length:
                logging.warning(f"Prompt length exceeds limit ({len(prompt)} > {max_prompt_length}), will truncate")
                # 截断提示词，保留系统消息和部分用户消息
                prompt = prompt[:max_prompt_length]
            
            # 使用LLM生成报告
            from langchain_core.messages import SystemMessage, HumanMessage
            msg = [SystemMessage(content="You are a rigorous computer science professor skilled in writing high-quality academic papers."), HumanMessage(content=prompt)]
            content = self.llm.chat(msg)
            
            # 使用项目名称作为文件名，先清理特殊字符
            import re
            timestamp = int(time.time())
            safe_project_name = re.sub(r'[\/*?:"<>|]', '_', project_name)  # 替换Windows和Linux的非法字符
            safe_project_name = safe_project_name.strip()
            if not safe_project_name:
                safe_project_name = f"code_report_{timestamp}"
            filename = f"{safe_project_name}.md"
            
            # 计算实际字数（中文按字符计算，英文按单词计算）
            def count_words(text):
                import re
                # 中文汉字
                chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
                # 英文单词
                english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
                # 数字
                numbers = len(re.findall(r'\b\d+\b', text))
                return chinese_chars + english_words + numbers
            
            actual_word_count = count_words(content)
            
            logging.info(f"✅ 报告已生成: {filename}")
            logging.info(f"📄 字符数: {len(content)}")
            logging.info(f"📄 实际字数: {actual_word_count}")
            
            return {
                "status": "success",
                "filename": filename,
                "content": content,
                "word_count": actual_word_count
            }
        except Exception as e:
            logging.error(f"❌ 生成报告失败: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
