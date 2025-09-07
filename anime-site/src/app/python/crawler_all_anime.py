#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫完整动漫列表爬虫 - API版本
爬取所有分类的动漫列表数据
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin
from typing import List, Dict
from datetime import datetime

class AllAnimeCrawler:
    """完整动漫列表爬虫"""
    
    def __init__(self, base_url: str = "http://m.iyinghua.com"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
    
    def crawl_all_anime(self, delay: float = 0.1) -> List[Dict]:
        """爬取所有分类的动漫列表
        
        Args:
            delay: 请求间隔时间(秒)
            
        Returns:
            所有动漫数据列表
        """
        url = f"{self.base_url}/all/"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                raise Exception(f"访问失败，状态码: {response.status_code}")
            
            return self._parse_all_anime(response.text, delay)
            
        except requests.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def _parse_all_anime(self, html_content: str, delay: float) -> List[Dict]:
        """解析所有动漫数据"""
        soup = BeautifulSoup(html_content, 'html.parser')
        all_anime_data = []
        
        # 查找所有分类
        mlist_divs = soup.find_all('div', class_='mlist')
        
        for category_idx, mlist_div in enumerate(mlist_divs, 1):
            # 获取分类名称
            category_name = f"分类{category_idx}"
            category_link = mlist_div.find('li', class_='man')
            if category_link and category_link.find('a'):
                category_name = category_link.find('a').get_text(strip=True)
            
            # 获取该分类下的所有动漫
            li_elements = mlist_div.find_all('li')
            
            for li in li_elements:
                try:
                    # 跳过分类标题行
                    if 'man' in li.get('class', []):
                        continue
                    
                    anime_data = {}
                    
                    # 提取标题和链接
                    title_link = li.find('a', target="_blank")
                    if not title_link:
                        all_links = li.find_all('a')
                        if all_links:
                            title_link = all_links[0]
                        else:
                            continue
                    
                    anime_data['title'] = title_link.get_text(strip=True)
                    anime_data['detail_url'] = urljoin(self.base_url, title_link.get('href', ''))
                    
                    # 提取集数信息
                    em_tag = li.find('em')
                    if em_tag:
                        episode_link = em_tag.find('a')
                        if episode_link:
                            anime_data['episode_info'] = episode_link.get_text(strip=True)
                            anime_data['episode_url'] = urljoin(self.base_url, episode_link.get('href', ''))
                        else:
                            anime_data['episode_info'] = em_tag.get_text(strip=True)
                            anime_data['episode_url'] = ""
                    else:
                        anime_data['episode_info'] = ""
                        anime_data['episode_url'] = ""
                    
                    anime_data['category'] = category_name
                    anime_data['full_text'] = li.get_text(strip=True)
                    
                    all_anime_data.append(anime_data)
                    
                except Exception as e:
                    continue
            
            # 避免请求过快
            time.sleep(delay)
        
        return all_anime_data

def get_all_anime(delay: float = 0.1) -> Dict:
    """获取所有动漫的API接口函数
    
    Args:
        delay: 请求间隔时间(秒)
        
    Returns:
        包含所有动漫数据的响应字典
    """
    crawler = AllAnimeCrawler()
    
    try:
        data = crawler.crawl_all_anime(delay)
        
        # 统计信息
        category_stats = {}
        for anime in data:
            category = anime.get('category', '未知')
            category_stats[category] = category_stats.get(category, 0) + 1
        
        return {
            'success': True,
            'total_count': len(data),
            'category_count': len(category_stats),
            'categories': category_stats,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'total_count': 0,
            'data': [],
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # 测试函数
    result = get_all_anime(delay=0.05)
    print(json.dumps(result, ensure_ascii=False, indent=2))