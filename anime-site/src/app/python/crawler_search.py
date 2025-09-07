#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫搜索爬虫 - API版本
爬取动漫搜索结果，支持关键词搜索
"""

import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
from typing import List, Dict, Optional
from datetime import datetime

class SearchCrawler:
    """搜索爬虫类"""
    
    def __init__(self, base_url: str = "http://www.iyinghua.com"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
    
    def search(self, keyword: str, max_results: int = 50) -> List[Dict]:
        """搜索动漫
        
        Args:
            keyword: 搜索关键词
            max_results: 最大返回结果数
            
        Returns:
            搜索结果列表
        """
        if not keyword.strip():
            return []
            
        try:
            encoded_keyword = urllib.parse.quote(keyword)
            search_url = f"{self.base_url}/search/{encoded_keyword}/"
            
            response = requests.get(search_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            return self._parse_search_results(response.text, keyword, max_results)
            
        except requests.RequestException as e:
            raise Exception(f"搜索失败: {str(e)}")
    
    def _parse_search_results(self, html_content: str, keyword: str, max_results: int) -> List[Dict]:
        """解析搜索结果"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # 查找搜索结果列表
        lpic_div = soup.find('div', class_='lpic')
        if not lpic_div:
            return results
            
        anime_items = lpic_div.find_all('li')
        
        for item in anime_items[:max_results]:
            try:
                anime_data = {}
                
                # 图片信息
                img_tag = item.find('img')
                if img_tag:
                    anime_data['cover_image'] = img_tag.get('src', '')
                    anime_data['title'] = img_tag.get('alt', '')
                
                # 标题和链接
                title_link = item.find('h2').find('a') if item.find('h2') else None
                if title_link:
                    anime_data['title'] = title_link.get_text(strip=True)
                    anime_data['detail_url'] = urllib.parse.urljoin(self.base_url, title_link.get('href', ''))
                
                # 集数信息
                spans = item.find_all('span')
                for span in spans:
                    span_text = span.get_text(strip=True)
                    if '集' in span_text:
                        anime_data['episodes'] = span_text
                        break
                
                # 类型信息
                anime_data['genres'] = []
                for span in spans:
                    span_text = span.get_text(strip=True)
                    if '类型：' in span_text:
                        type_text = span_text.replace('类型：', '').strip()
                        if type_text:
                            anime_data['genres'] = [t.strip() for t in type_text.split('，')]
                        break
                
                # 描述
                desc_p = item.find('p')
                if desc_p:
                    anime_data['description'] = desc_p.get_text(strip=True)
                else:
                    anime_data['description'] = ""
                
                # 搜索元数据
                anime_data['search_keyword'] = keyword
                anime_data['search_time'] = datetime.now().isoformat()
                
                if anime_data.get('title'):
                    results.append(anime_data)
                    
            except Exception as e:
                continue
        
        return results

def search_anime(keyword: str, max_results: int = 50) -> Dict:
    """搜索动漫的API接口函数
    
    Args:
        keyword: 搜索关键词
        max_results: 最大返回结果数
        
    Returns:
        包含搜索结果的响应字典
    """
    crawler = SearchCrawler()
    
    try:
        results = crawler.search(keyword, max_results)
        
        return {
            'success': True,
            'keyword': keyword,
            'total_count': len(results),
            'data': results,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'keyword': keyword,
            'data': [],
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # 测试函数
    result = search_anime("百妖谱")
    print(json.dumps(result, ensure_ascii=False, indent=2))