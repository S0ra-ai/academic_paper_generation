import os
import logging
from typing import List, Set, Dict, Tuple
from pathlib import Path
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KeywordMatch:
    """关键词匹配结果"""
    keyword: str
    category: str
    match_type: str  # 'exact' or 'fuzzy'
    position: int
    context: str


class SensitiveLexiconLoader:
    """敏感词加载器 - 全量加载 + 混合匹配"""
    
    def __init__(self, lexicon_path: str = None):
        if lexicon_path is None:
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent.parent
            lexicon_path = project_root / "Sensitive-lexicon" / "Vocabulary"
            
            if not lexicon_path.exists():
                lexicon_path = Path.cwd().parent / "Sensitive-lexicon" / "Vocabulary"
        
        self.lexicon_path = Path(lexicon_path)
        self.all_keywords: Set[str] = set()
        self.categorized_keywords: Dict[str, Set[str]] = {}
        self.core_keywords: Set[str] = set()
        self.trie: Dict = {}
        
        self._load_all_lexicons()
        self._identify_core_keywords()
        self._build_trie()
    
    def _load_all_lexicons(self):
        """全量加载所有词库"""
        if not self.lexicon_path.exists():
            logger.warning(f"词库路径不存在: {self.lexicon_path}")
            return
        
        loaded_files = []
        
        for file_path in self.lexicon_path.glob("*.txt"):
            category = file_path.stem
            self._load_lexicon_file(file_path, category)
            loaded_files.append(category)
        
        logger.info(f"全量加载完成: {len(loaded_files)} 个分类, 共 {len(self.all_keywords)} 个敏感词")
        logger.info(f"分类列表: {', '.join(loaded_files)}")
    
    def _load_lexicon_file(self, file_path: Path, category: str):
        """加载单个词库文件"""
        try:
            count = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.all_keywords.add(line)
                        
                        if category not in self.categorized_keywords:
                            self.categorized_keywords[category] = set()
                        self.categorized_keywords[category].add(line)
                        count += 1
            
            logger.info(f"加载 {category}: {count} 个词")
        
        except Exception as e:
            logger.error(f"加载词库失败 {file_path}: {str(e)}")
    
    def _identify_core_keywords(self):
        """识别核心关键词（需要精确匹配的词）"""
        core_categories = [
            "暴恐词库", "色情词库", "涉枪涉爆"
        ]
        
        for category in core_categories:
            if category in self.categorized_keywords:
                self.core_keywords.update(self.categorized_keywords[category])
        
        logger.info(f"核心关键词: {len(self.core_keywords)} 个")
    
    def _build_trie(self):
        """构建 Trie 树用于高效匹配"""
        for keyword in self.all_keywords:
            node = self.trie
            for char in keyword:
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['#'] = True
        
        logger.info(f"Trie 树构建完成")
    
    def check_text(self, text: str) -> List[KeywordMatch]:
        """检查文本中的敏感词（混合匹配）"""
        matches = []
        
        for category, keywords in self.categorized_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    match_type = 'exact' if keyword in self.core_keywords else 'fuzzy'
                    
                    index = text.find(keyword)
                    start = max(0, index - 10)
                    end = min(len(text), index + len(keyword) + 10)
                    context = text[start:end]
                    
                    matches.append(KeywordMatch(
                        keyword=keyword,
                        category=category,
                        match_type=match_type,
                        position=index,
                        context=context
                    ))
        
        return matches
    
    def get_all_keywords(self) -> Set[str]:
        """获取所有敏感词"""
        return self.all_keywords.copy()
    
    def get_category_keywords(self, category: str) -> Set[str]:
        """获取指定分类的敏感词"""
        return self.categorized_keywords.get(category, set()).copy()
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(self.categorized_keywords.keys())
    
    def is_core_keyword(self, keyword: str) -> bool:
        """判断是否为核心关键词"""
        return keyword in self.core_keywords


global_lexicon_loader = None


def init_lexicon_loader(lexicon_path: str = None) -> SensitiveLexiconLoader:
    """初始化全局词库加载器"""
    global global_lexicon_loader
    global_lexicon_loader = SensitiveLexiconLoader(lexicon_path)
    return global_lexicon_loader


def get_lexicon_loader() -> SensitiveLexiconLoader:
    """获取全局词库加载器"""
    global global_lexicon_loader
    if global_lexicon_loader is None:
        global_lexicon_loader = SensitiveLexiconLoader()
    return global_lexicon_loader
