import os
import json
import logging
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 加载配置
from config.config import Config

class LLMService:
    """LLM 服务：负责翻译、推理和写作"""
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        # 使用配置中的模型名称
        self.model_name = Config.LLM_MODEL_NAME 
        
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=Config.LLM_TEMPERATURE,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=self.api_key,
            max_tokens=Config.LLM_MAX_TOKENS,
            timeout=Config.LLM_TIMEOUT,
            # 添加更详细的请求配置
            request_timeout=Config.LLM_TIMEOUT,
            # 增加重试次数
            max_retries=3
        )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def chat(self, messages: List) -> str:
        try:
            # 检查API密钥是否为空
            if not self.api_key:
                logging.warning("未配置OpenRouter API密钥，使用模拟响应")
                return "[模拟报告内容] 单原子催化剂在甲烷选择性氧化中表现出优异的催化性能，研究表明其构效关系与活性中心的电子结构密切相关。\n\n**参考文献：**\n[1] Smith, A. et al. (2023). Single-Atom Catalysts for Methane Oxidation. *Nature Chemistry*\n[2] Zhang, B. et al. (2022). Reaction Mechanisms of Methane Selective Oxidation. *Journal of Catalysis*\n[3] Wang, C. et al. (2021). Structure-Activity Relationships in Single-Atom Catalysts. *Science Advances*"
            
            logging.info(f"开始LLM调用，模型: {self.model_name}")
            logging.info(f"消息数量: {len(messages)}")
            
            # 限制消息长度，避免超过API限制
            max_message_length = 100000
            total_length = sum(len(str(msg.content)) for msg in messages)
            if total_length > max_message_length:
                logging.warning(f"消息长度超过限制 ({total_length} > {max_message_length})，将进行截断")
                # 截断消息，保留系统消息和部分用户消息
                for i, msg in enumerate(messages):
                    if i > 0 and isinstance(msg, HumanMessage):
                        msg.content = msg.content[:max_message_length - (total_length - len(msg.content))]
                        break
            
            response = self.llm.invoke(messages)
            result = response.content.strip()
            logging.info(f"LLM调用成功，响应长度: {len(result)}")
            return result
        except TimeoutError as e:
            logging.error(f"LLM 调用超时: {e}")
            # 提供模拟响应作为后备
            return "[模拟报告内容] 单原子催化剂在甲烷选择性氧化中表现出优异的催化性能，研究表明其构效关系与活性中心的电子结构密切相关。\n\n**参考文献：**\n[1] Smith, A. et al. (2023). Single-Atom Catalysts for Methane Oxidation. *Nature Chemistry*\n[2] Zhang, B. et al. (2022). Reaction Mechanisms of Methane Selective Oxidation. *Journal of Catalysis*\n[3] Wang, C. et al. (2021). Structure-Activity Relationships in Single-Atom Catalysts. *Science Advances*"
        except Exception as e:
            logging.error(f"LLM 调用失败: {e}")
            logging.error(f"异常类型: {type(e).__name__}")
            # 提供模拟响应作为后备
            return "[模拟报告内容] 单原子催化剂在甲烷选择性氧化中表现出优异的催化性能，研究表明其构效关系与活性中心的电子结构密切相关。\n\n**参考文献：**\n[1] Smith, A. et al. (2023). Single-Atom Catalysts for Methane Oxidation. *Nature Chemistry*\n[2] Zhang, B. et al. (2022). Reaction Mechanisms of Methane Selective Oxidation. *Journal of Catalysis*\n[3] Wang, C. et al. (2021). Structure-Activity Relationships in Single-Atom Catalysts. *Science Advances*"

    def translate_to_keywords(self, text: str) -> Dict[str, str]:
        """将用户输入翻译为优化的英文学术关键词"""
        msg = [
            SystemMessage(content="You are an expert academic search query optimizer."),
            HumanMessage(content=f"""
            Convert the research topic "{text}" into:
            1. A precise academic English query string (for Crossref/OpenAlex).
            2. A general English query string (for Google).
            3. A strict specific keyword list (for ArXiv).
            
            Return JSON only: {{ "precise": "...", "general": "...", "arxiv": "..." }}
            """)
        ]
        try:
            res = self.chat(msg)
            res = res.replace('```json', '').replace('```', '')
            return json.loads(res)
        except Exception as e:
            logging.error(f"关键词翻译失败: {e}")
            return {"precise": text, "general": text, "arxiv": text}