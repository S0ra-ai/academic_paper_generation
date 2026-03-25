import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

from .sensitive_lexicon_loader import get_lexicon_loader, KeywordMatch
from .semantic_analyzer import get_semantic_analyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SafetyCheckResult:
    """安全检查结果"""
    is_safe: bool
    risk_level: str  # 'safe', 'low', 'medium', 'high', 'critical'
    action: str  # 'allow', 'warn', 'review', 'block'
    detected_keywords: List[str]
    categories: List[str]
    message: str
    semantic_analysis: Dict
    timestamp: str
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "is_safe": self.is_safe,
            "risk_level": self.risk_level,
            "action": self.action,
            "detected_keywords": self.detected_keywords,
            "categories": self.categories,
            "message": self.message,
            "semantic_analysis": self.semantic_analysis,
            "timestamp": self.timestamp
        }


class ContentSafetyChecker:
    """内容安全检查器 - 混合方案"""
    
    def __init__(self):
        self.lexicon_loader = get_lexicon_loader()
        self.semantic_analyzer = get_semantic_analyzer()
        
        self.strict_categories = ["暴恐词库", "色情词库", "色情类型", "涉枪涉爆", "反动词库"]
        self.review_categories = ["政治类型", "贪腐词库", "GFW补充词库"]
        self.warn_categories = ["广告类型", "其他词库", "民生词库"]
        
        self.critical_keywords = {
            "色情", "恐怖", "暴恐", "毒品", "枪支", "爆炸", 
            "恐怖袭击", "恐怖主义", "制造毒品", "制毒"
        }
        
        logger.info("内容安全检查器初始化完成")
    
    def check_input(self, text: str, user_id: str = None) -> SafetyCheckResult:
        """检查输入内容"""
        return self._check_content(text, "input", user_id)
    
    def check_output(self, text: str, user_id: str = None) -> SafetyCheckResult:
        """检查输出内容"""
        return self._check_content(text, "output", user_id)
    
    def _check_content(self, text: str, check_type: str, user_id: str = None) -> SafetyCheckResult:
        """执行内容检查"""
        logger.info(f"开始检查{check_type}内容，长度: {len(text)}")
        
        keyword_matches = self.lexicon_loader.check_text(text)
        
        if not keyword_matches:
            return SafetyCheckResult(
                is_safe=True,
                risk_level="safe",
                action="allow",
                detected_keywords=[],
                categories=[],
                message=f"{check_type}内容安全检查通过",
                semantic_analysis={},
                timestamp=datetime.now().isoformat()
            )
        
        semantic_result = self.semantic_analyzer.analyze(text)
        
        risk_level, action, message = self._determine_risk(
            keyword_matches, 
            semantic_result,
            text
        )
        
        detected_keywords = list(set([m.keyword for m in keyword_matches]))
        categories = list(set([m.category for m in keyword_matches]))
        
        self._log_safety_event(
            check_type, 
            text, 
            keyword_matches, 
            semantic_result,
            risk_level,
            user_id
        )
        
        is_safe = action in ["allow", "warn"]
        
        return SafetyCheckResult(
            is_safe=is_safe,
            risk_level=risk_level,
            action=action,
            detected_keywords=detected_keywords,
            categories=categories,
            message=message,
            semantic_analysis=semantic_result,
            timestamp=datetime.now().isoformat()
        )
    
    def _determine_risk(
        self, 
        keyword_matches: List[KeywordMatch],
        semantic_result: Dict,
        text: str
    ) -> Tuple[str, str, str]:
        """确定风险等级"""
        
        critical_keywords = []
        high_keywords = []
        medium_keywords = []
        low_keywords = []
        
        generation_patterns = [
            "请帮我写", "帮我写", "写一篇", "生成", "创作",
            "如何制作", "怎么制作", "制作方法", "详细步骤"
        ]
        
        is_generation_request = any(pattern in text for pattern in generation_patterns)
        
        for match in keyword_matches:
            is_critical = match.keyword in self.critical_keywords
            
            if is_critical and is_generation_request:
                critical_keywords.append((match.keyword, match.category))
                continue
            
            is_safe_context, reason = self.semantic_analyzer.is_safe_context(
                text, 
                match.keyword
            )
            
            if is_critical and not is_safe_context:
                critical_keywords.append((match.keyword, match.category))
            elif match.match_type == 'exact' and not is_safe_context:
                if match.category in self.strict_categories:
                    critical_keywords.append((match.keyword, match.category))
                else:
                    high_keywords.append((match.keyword, match.category))
            elif is_safe_context:
                low_keywords.append((match.keyword, match.category, reason))
            else:
                if match.category in self.review_categories:
                    medium_keywords.append((match.keyword, match.category))
                else:
                    low_keywords.append((match.keyword, match.category, "非安全语境"))
        
        if critical_keywords:
            keywords_str = ', '.join([k[0] for k in critical_keywords[:3]])
            return (
                "critical",
                "block",
                f"检测到绝对禁止内容: {keywords_str}"
            )
        
        if high_keywords:
            keywords_str = ', '.join([k[0] for k in high_keywords[:3]])
            return (
                "high",
                "block",
                f"检测到高风险内容: {keywords_str}"
            )
        
        if medium_keywords:
            if semantic_result.get("is_malicious_intent"):
                keywords_str = ', '.join([k[0] for k in medium_keywords[:3]])
                return (
                    "high",
                    "block",
                    f"检测到恶意意图: {keywords_str}"
                )
            
            keywords_str = ', '.join([k[0] for k in medium_keywords[:3]])
            return (
                "medium",
                "review",
                f"检测到需审核内容: {keywords_str}"
            )
        
        if low_keywords:
            keywords_str = ', '.join([k[0] for k in low_keywords[:3]])
            return (
                "low",
                "warn",
                f"检测到潜在风险内容: {keywords_str}"
            )
        
        return ("safe", "allow", "内容安全检查通过")
    
    def _log_safety_event(
        self,
        check_type: str,
        text: str,
        keyword_matches: List[KeywordMatch],
        semantic_result: Dict,
        risk_level: str,
        user_id: str = None
    ):
        """记录安全事件"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "check_type": check_type,
            "user_id": user_id,
            "text_length": len(text),
            "text_preview": text[:100] if len(text) > 100 else text,
            "detected_keywords": [
                {
                    "keyword": m.keyword,
                    "category": m.category,
                    "match_type": m.match_type
                } for m in keyword_matches[:10]
            ],
            "semantic_analysis": {
                "is_academic": semantic_result.get("is_academic_context"),
                "is_negative": semantic_result.get("is_negative_context"),
                "is_quote": semantic_result.get("is_quote_context"),
                "is_malicious": semantic_result.get("is_malicious_intent"),
                "sentiment": semantic_result.get("sentiment_score")
            },
            "risk_level": risk_level
        }
        
        logger.warning(f"安全事件: {json.dumps(log_data, ensure_ascii=False)}")
        
        try:
            with open('safety_events.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_data, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"写入安全日志失败: {str(e)}")
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "total_keywords": len(self.lexicon_loader.get_all_keywords()),
            "categories": len(self.lexicon_loader.get_categories()),
            "core_keywords": len(self.lexicon_loader.core_keywords),
            "category_details": {
                category: len(keywords) 
                for category, keywords in self.lexicon_loader.categorized_keywords.items()
            }
        }


global_safety_checker = None


def init_safety_checker() -> ContentSafetyChecker:
    """初始化全局安全检查器"""
    global global_safety_checker
    global_safety_checker = ContentSafetyChecker()
    return global_safety_checker


def get_safety_checker() -> ContentSafetyChecker:
    """获取全局安全检查器"""
    global global_safety_checker
    if global_safety_checker is None:
        global_safety_checker = ContentSafetyChecker()
    return global_safety_checker


def check_content_safety(text: str, content_type: str = "input", user_id: str = None) -> SafetyCheckResult:
    """便捷函数：检查内容安全"""
    checker = get_safety_checker()
    if content_type == "input":
        return checker.check_input(text, user_id)
    else:
        return checker.check_output(text, user_id)
