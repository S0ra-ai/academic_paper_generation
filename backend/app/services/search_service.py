import os
import re
import time
import logging
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
from urllib3.exceptions import InsecureRequestWarning
from langchain_community.utilities import ArxivAPIWrapper

# 加载配置
from config.config import Config

# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class UnifiedAcademicSearcher:
    """
    统一学术搜索器：聚合 Crossref, OpenAlex, ArXiv, Semantic Scholar, Google
    """
    def __init__(self):
        self.serp_key = Config.SERPAPI_KEY
        self.email = Config.ACADEMIC_EMAIL or "test@example.com"
        
        # 统一请求头，用于 Crossref 和 OpenAlex 的 Polite Pool
        self.headers = {
            "User-Agent": f"AcademicReportBot/3.0 (mailto:{self.email})"
        }
    
    def _normalize_result(self, title, authors, year, snippet, url, source):
        """标准化返回格式"""
        return {
            "title": str(title).strip(),
            "authors": str(authors).strip(),
            "year": str(year),
            "snippet": str(snippet).strip().replace('\n', ' ')[:600],
            "link": url,
            "source": source
        }

    def search_crossref(self, query: str, limit=6) -> List[Dict]:
        """
        Crossref API: 官方 DOI 注册库，元数据极其规范
        """
        api_url = "https://api.crossref.org/works"
        params = {
            "query.bibliographic": query,
            "rows": limit,
            "sort": "relevance",
            "select": "title,author,published,abstract,URL,container-title,DOI"
        }
        
        # 手动实现重试逻辑，确保方法总是返回列表
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"🔍 [Crossref] 搜索: {query} (尝试 {attempt+1}/{max_retries})")
                # Crossref 有时响应较慢，timeout 设长一点
                resp = requests.get(api_url, params=params, headers=self.headers, timeout=15)
                
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get('message', {}).get('items', [])
                    results = []
                    
                    for item in items:
                        # 提取标题
                        title = item.get('title', ['Unknown Title'])[0]
                        
                        # 提取作者
                        authors_list = []
                        for a in item.get('author', [])[:3]:
                            name = f"{a.get('given', '')} {a.get('family', '')}".strip()
                            if name: authors_list.append(name)
                        authors = ", ".join(authors_list)
                        
                        # 提取年份
                        try:
                            year = item.get('published', {}).get('date-parts', [[None]])[0][0]
                        except:
                            year = "N/A"
                            
                        # 提取摘要或补充信息 (Crossref 摘要经常是 XML 格式或缺失，做一下处理)
                        abstract = item.get('abstract', '')
                        if abstract:
                            # 简单去除 XML 标签
                            abstract = re.sub(r'<[^>]+>', '', abstract)
                        else:
                            journal = item.get('container-title', [''])[0]
                            abstract = f"Published in {journal}. DOI: {item.get('DOI')}"
                        
                        results.append(self._normalize_result(
                            title=title,
                            authors=authors,
                            year=year,
                            snippet=abstract,
                            url=item.get('URL') or f"https://doi.org/{item.get('DOI')}",
                            source="Crossref API"
                        ))
                    
                    logging.info(f"   ✅ [Crossref] 找到 {len(results)} 篇")
                    return results
                    
            except Exception as e:
                logging.warning(f"⚠️ [Crossref] 尝试 {attempt+1}/{max_retries} 失败: {e}")
                # 如果不是最后一次尝试，等待一段时间后重试
                if attempt < max_retries - 1:
                    wait_time = min(2 ** (attempt + 1), 10)  # 指数退避，最大等待10秒
                    logging.info(f"   ⏳ [Crossref] {wait_time}秒后重试...")
                    time.sleep(wait_time)
        return []

    def search_openalex(self, query: str, limit=6) -> List[Dict]:
        """[免费] OpenAlex API"""
        api_url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "sort": "relevance_score:desc",
            "per_page": limit,
            "filter": f"from_publication_date:{datetime.now().year-5}-01-01"
        }
        
        # 手动实现重试逻辑，确保方法总是返回列表
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"🔍 [OpenAlex] 搜索: {query} (尝试 {attempt+1}/{max_retries})")
                resp = requests.get(api_url, params=params, headers=self.headers, timeout=10)
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        if not isinstance(data, dict):
                            logging.warning(f"[OpenAlex] 无效的JSON响应格式: {data}")
                            continue
                        results = []
                        for item in data.get('results', []):
                            authors = ", ".join([a.get('author', {}).get('display_name', 'Unknown Author') for a in item.get('authorships', []) if a is not None][:3])
                            concepts = ", ".join([c.get('display_name', '') for c in item.get('concepts', []) if c is not None][:5])
                            journal = item.get('primary_location', {}).get('source', {}).get('display_name', 'N/A')
                            snippet = f"Key Concepts: {concepts}. Journal: {journal}"
                            
                            results.append(self._normalize_result(
                                title=item.get('title', 'Unknown Title'),
                                authors=authors,
                                year=item.get('publication_year', 'N/A'),
                                snippet=snippet,
                                url=item.get('doi') or item.get('id', ''),
                                source="OpenAlex"
                            ))
                        logging.info(f"   ✅ [OpenAlex] 找到 {len(results)} 篇")
                        return results
                    except Exception as inner_e:
                        logging.warning(f"[OpenAlex] 处理响应时出错: {inner_e}")
            except Exception as e:
                logging.warning(f"⚠️ [OpenAlex] 尝试 {attempt+1}/{max_retries} 失败: {e}")
                # 如果不是最后一次尝试，等待一段时间后重试
                if attempt < max_retries - 1:
                    wait_time = min(2 ** (attempt + 1), 10)  # 指数退避，最大等待10秒
                    logging.info(f"   ⏳ [OpenAlex] {wait_time}秒后重试...")
                    time.sleep(wait_time)
        return []

    def search_arxiv(self, query: str, limit=5) -> List[Dict]:
        """[免费] ArXiv API"""
        # 手动实现重试逻辑，确保方法总是返回列表
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"🔍 [ArXiv] 搜索: {query} (尝试 {attempt+1}/{max_retries})")
                # ArXiv API可能不支持中文，使用英文关键词或简化查询
                # 如果查询包含中文，只取前几个字符或使用通用术语
                if any(ord(c) > 127 for c in query):
                    query = "methane selective oxidation single atom catalyst"  # 英文替代查询
                arxiv = ArxivAPIWrapper(top_k_results=limit, doc_content_chars_max=1000)
                docs = arxiv.load(query)
                
                results = []
                for doc in docs:
                    results.append(self._normalize_result(
                        title=doc.metadata.get('Title', 'Unknown'),
                        authors=doc.metadata.get('Authors', 'ArXiv Author'),
                        year=doc.metadata.get('Published', 'Recent'),
                        snippet=doc.page_content,
                        url=doc.metadata.get('Entry ID', ''),
                        source="ArXiv"
                    ))
                logging.info(f"   ✅ [ArXiv] 找到 {len(results)} 篇")
                return results
            except Exception as e:
                logging.warning(f"⚠️ [ArXiv] 尝试 {attempt+1}/{max_retries} 失败: {e}")
                # 如果不是最后一次尝试，等待一段时间后重试
                if attempt < max_retries - 1:
                    wait_time = min(2 ** (attempt + 1), 10)  # 指数退避，最大等待10秒
                    logging.info(f"   ⏳ [ArXiv] {wait_time}秒后重试...")
                    time.sleep(wait_time)
        return []

    def search_semantic_scholar_public(self, query: str, limit=5) -> List[Dict]:
        """[半免费] Semantic Scholar"""
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "year": f"{datetime.now().year-5}-{datetime.now().year}",
            "fields": "title,abstract,year,authors,url,venue"
        }
        
        # 手动实现重试逻辑，确保方法总是返回列表
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"🔍 [S2] 搜索: {query} (尝试 {attempt+1}/{max_retries})")
                time.sleep(1.0) 
                resp = requests.get(url, params=params, timeout=10)
                
                if resp.status_code == 200:
                    data = resp.json().get('data', [])
                    results = []
                    for paper in data:
                        authors = ", ".join([a['name'] for a in paper.get('authors', [])[:3]])
                        results.append(self._normalize_result(
                            title=paper.get('title'),
                            authors=authors,
                            year=paper.get('year'),
                            snippet=paper.get('abstract') or "No abstract available.",
                            url=paper.get('url'),
                            source="Semantic Scholar"
                        ))
                    logging.info(f"   ✅ [S2] 找到 {len(results)} 篇")
                    return results
            except Exception as e:
                logging.warning(f"⚠️ [S2] 尝试 {attempt+1}/{max_retries} 失败: {e}")
                # 如果不是最后一次尝试，等待一段时间后重试
                if attempt < max_retries - 1:
                    wait_time = min(2 ** (attempt + 1), 10)  # 指数退避，最大等待10秒
                    logging.info(f"   ⏳ [S2] {wait_time}秒后重试...")
                    time.sleep(wait_time)
        return []

    def search_google_serp(self, query: str, limit=4) -> List[Dict]:
        """[API Key] Google Serps"""
        if not self.serp_key: return []
        
        # 手动实现重试逻辑，确保方法总是返回列表
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"🔍 [Google] 搜索: {query} (尝试 {attempt+1}/{max_retries})")
                params = {
                    "q": query,
                    "api_key": self.serp_key,
                    "engine": "google_scholar",
                    "num": limit,
                    "hl": "zh-CN",
                    "as_ylo": datetime.now().year - 4
                }
                resp = requests.get("https://serpapi.com/search", params=params, timeout=20)
                data = resp.json()
                results = []
                if "organic_results" in data:
                    for item in data["organic_results"]:
                        results.append(self._normalize_result(
                            title=item.get("title"),
                            authors="Google Scholar Result",
                            year="Recent",
                            snippet=item.get("snippet", ""),
                            url=item.get("link"),
                            source="Google Scholar"
                        ))
                logging.info(f"   ✅ [Google] 找到 {len(results)} 篇")
                return results
            except Exception as e:
                logging.warning(f"⚠️ [Google] 尝试 {attempt+1}/{max_retries} 失败: {e}")
                # 如果不是最后一次尝试，等待一段时间后重试
                if attempt < max_retries - 1:
                    wait_time = min(2 ** (attempt + 1), 10)  # 指数退避，最大等待10秒
                    logging.info(f"   ⏳ [Google] {wait_time}秒后重试...")
                    time.sleep(wait_time)
        return []

    def run_ensemble_search(self, topic_query: Dict[str, str], limit=10) -> List[Dict]:
        """并发执行所有搜索"""
        all_results = []
        
        # 定义任务列表：增加 Crossref
        tasks = [
            (self.search_crossref, topic_query["precise"], limit), # 新增 Crossref
            (self.search_openalex, topic_query["precise"], limit),
            (self.search_arxiv, topic_query["arxiv"], limit),
            (self.search_semantic_scholar_public, topic_query["precise"], limit),
            (self.search_google_serp, topic_query["general"], limit)
        ]

        logging.info("🚀 开始全网并发检索 (含 Crossref)...")
        # 控制并发数，避免资源耗尽
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_source = {executor.submit(func, q, limit): func.__name__ for func, q, limit in tasks}
            
            for future in as_completed(future_to_source):
                try:
                    res = future.result()
                    all_results.extend(res)
                except Exception as e:
                    # 捕获所有异常，包括RetryError，确保不会影响其他任务
                    logging.error(f"源 {future_to_source[future]} 执行失败: {e}")
                    # 继续执行其他任务，不中断整个搜索过程

        # 去重逻辑
        seen_titles = set()
        unique_results = []
        for r in all_results:
            # 去除标点和空格进行比较
            norm_title = "".join(filter(str.isalnum, r['title'].lower()))
            if norm_title not in seen_titles and len(norm_title) > 10:
                seen_titles.add(norm_title)
                unique_results.append(r)
        
        logging.info(f"📊 检索完成。原始结果: {len(all_results)} -> 去重后: {len(unique_results)}")
        return unique_results