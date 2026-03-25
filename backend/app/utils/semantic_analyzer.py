import jieba
import jieba.posseg as pseg
from snownlp import SnowNLP
import logging
from typing import List, Dict, Tuple
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SemanticAnalyzer:
    """语义分析器 - 基于 jieba + SnowNLP"""
    
    def __init__(self):
        self._init_jieba()
        self._init_context_rules()
        logger.info("语义分析器初始化完成")
    
    def _init_jieba(self):
        """初始化 jieba 分词"""
        jieba.initialize()
        logger.info("jieba 分词器初始化完成")
    
    def _init_context_rules(self):
        """初始化上下文规则"""
        self.academic_context_keywords = [
            "研究", "分析", "探讨", "论文", "学术", "理论",
            "调查", "报告", "实验", "数据", "案例", "文献"
        ]
        
        self.negative_context_keywords = [
            "不", "禁止", "反对", "批判", "否定", "拒绝",
            "防止", "避免", "杜绝", "制止", "打击"
        ]
        
        self.quote_patterns = [
            r'《(.+?)》',
            r'"(.+?)"',
            r'「(.+?)」',
            r'引用(.+?)',
            r'根据(.+?)'
        ]
        
        self.malicious_intent_patterns = [
            r'如何.*制作',
            r'怎么.*制造',
            r'方法.*步骤',
            r'教程.*指南',
            r'完整.*流程'
        ]
    
    def analyze(self, text: str) -> Dict:
        """综合语义分析"""
        result = {
            "is_academic_context": False,
            "is_negative_context": False,
            "is_quote_context": False,
            "is_malicious_intent": False,
            "sentiment_score": 0.5,
            "keywords": [],
            "pos_tags": [],
            "analysis_details": {}
        }
        
        try:
            result["is_academic_context"] = self._check_academic_context(text)
            result["is_negative_context"] = self._check_negative_context(text)
            result["is_quote_context"] = self._check_quote_context(text)
            result["is_malicious_intent"] = self._check_malicious_intent(text)
            result["sentiment_score"] = self._analyze_sentiment(text)
            result["keywords"] = self._extract_keywords(text)
            result["pos_tags"] = self._pos_tagging(text)
            
            result["analysis_details"] = {
                "academic_score": self._calculate_academic_score(text),
                "negative_score": self._calculate_negative_score(text),
                "intent_score": self._calculate_intent_score(text)
            }
        
        except Exception as e:
            logger.error(f"语义分析失败: {str(e)}")
        
        return result
    
    def _check_academic_context(self, text: str) -> bool:
        """检查是否为学术语境"""
        strong_academic_keywords = [
            "研究", "分析", "探讨", "论文", "学术", "理论",
            "调查", "报告", "实验", "数据", "案例", "文献",
            "历史背景", "社会影响", "影响分析", "背景分析"
        ]
        
        for keyword in strong_academic_keywords:
            if keyword in text:
                return True
        
        count = sum(1 for keyword in self.academic_context_keywords if keyword in text)
        return count >= 2
    
    def _check_negative_context(self, text: str) -> bool:
        """检查是否为否定语境"""
        for keyword in self.negative_context_keywords:
            if keyword in text:
                return True
        return False
    
    def _check_quote_context(self, text: str) -> bool:
        """检查是否为引用语境"""
        for pattern in self.quote_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _check_malicious_intent(self, text: str) -> bool:
        """检查是否为恶意意图"""
        for pattern in self.malicious_intent_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _analyze_sentiment(self, text: str) -> float:
        """情感分析"""
        try:
            s = SnowNLP(text)
            return s.sentiments
        except Exception as e:
            logger.warning(f"情感分析失败: {str(e)}")
            return 0.5
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        try:
            s = SnowNLP(text)
            return s.keywords(5)
        except Exception as e:
            logger.warning(f"关键词提取失败: {str(e)}")
            return []
    
    def _pos_tagging(self, text: str) -> List[Tuple[str, str]]:
        """词性标注"""
        try:
            words = pseg.cut(text)
            return [(word, flag) for word, flag in words if len(word) > 1]
        except Exception as e:
            logger.warning(f"词性标注失败: {str(e)}")
            return []
    
    def _calculate_academic_score(self, text: str) -> float:
        """计算学术语境得分"""
        count = sum(1 for keyword in self.academic_context_keywords if keyword in text)
        return min(count / len(self.academic_context_keywords), 1.0)
    
    def _calculate_negative_score(self, text: str) -> float:
        """计算否定语境得分"""
        count = sum(1 for keyword in self.negative_context_keywords if keyword in text)
        return min(count / len(self.negative_context_keywords), 1.0)
    
    def _calculate_intent_score(self, text: str) -> float:
        """计算恶意意图得分"""
        count = sum(1 for pattern in self.malicious_intent_patterns if re.search(pattern, text))
        return min(count / len(self.malicious_intent_patterns), 1.0)
    
    def check_context_around_keyword(self, text: str, keyword: str, window_size: int = 30) -> Dict:
        """检查关键词周围的上下文"""
        index = text.find(keyword)
        if index == -1:
            return {"found": False}
        
        start = max(0, index - window_size)
        end = min(len(text), index + len(keyword) + window_size)
        context = text[start:end]
        
        full_text_analysis = {
            "is_academic": self._check_academic_context(text),
            "is_negative": self._check_negative_context(text),
            "is_quote": self._check_quote_context(text),
        }
        
        context_analysis = {
            "is_academic": self._check_academic_context(context),
            "is_negative": self._check_negative_context(context),
            "is_quote": self._check_quote_context(context),
        }
        
        return {
            "found": True,
            "context": context,
            "is_academic": full_text_analysis["is_academic"] or context_analysis["is_academic"],
            "is_negative": full_text_analysis["is_negative"] or context_analysis["is_negative"],
            "is_quote": full_text_analysis["is_quote"] or context_analysis["is_quote"],
            "sentiment": self._analyze_sentiment(context)
        }
    
    def is_safe_context(self, text: str, keyword: str) -> Tuple[bool, str]:
        """判断关键词是否在安全上下文中"""
        context_info = self.check_context_around_keyword(text, keyword)
        
        if not context_info["found"]:
            return False, "关键词未找到"
        
        reasons = []
        
        if context_info["is_academic"]:
            reasons.append("学术语境")
        
        if context_info["is_negative"]:
            reasons.append("否定表达")
        
        if context_info["is_quote"]:
            reasons.append("引用内容")
        
        if context_info["sentiment"] < 0.3:
            reasons.append("负面情感")
        
        if reasons:
            return True, f"安全语境: {', '.join(reasons)}"
        
        return False, "非安全语境"


global_semantic_analyzer = None


def init_semantic_analyzer() -> SemanticAnalyzer:
    """初始化全局语义分析器"""
    global global_semantic_analyzer
    global_semantic_analyzer = SemanticAnalyzer()
    return global_semantic_analyzer


def get_semantic_analyzer() -> SemanticAnalyzer:
    """获取全局语义分析器"""
    global global_semantic_analyzer
    if global_semantic_analyzer is None:
        global_semantic_analyzer = SemanticAnalyzer()
    return global_semantic_analyzer
