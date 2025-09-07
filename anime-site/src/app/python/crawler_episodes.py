#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫分集URL爬虫 - API版本
爬取动漫详情页的分集列表
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin
from typing import List, Dict, Optional
from datetime import datetime

class EpisodesCrawler:
    """分集URL爬虫类"""
    
    def __init__(self, base_url: str = "http://www.iyinghua.com"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
    
    def crawl_episodes(self, anime_url: str) -> List[Dict]:
        """爬取动漫分集信息
        
        Args:
            anime_url: 动漫详情页URL
            
        Returns:
            分集信息列表
        """
        if not self._validate_url(anime_url):
            raise ValueError("无效的动漫页面URL")
        
        try:
            response = requests.get(anime_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取动漫标题
            anime_title = self._extract_anime_title(soup)
            
            # 提取分集信息
            episodes = self._extract_episodes(soup)
            
            # 添加动漫标题到每个分集
            for episode in episodes:
                episode['anime_title'] = anime_title
                episode['anime_url'] = anime_url
            
            return episodes
            
        except requests.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
    
    def _validate_url(self, url: str) -> bool:
        """验证URL格式"""
        if not url:
            return False
        if 'iyinghua.com' not in url:
            return False
        if not url.startswith('http'):
            return False
        return True
    
    def _extract_anime_title(self, soup: BeautifulSoup) -> str:
        """提取动漫标题"""
        title = "未知动漫"
        
        # 尝试多种方式获取标题
        title_elem = soup.find('h1')
        if title_elem:
            title = title_elem.get_text().strip()
        else:
            title_elem = soup.find('title')
            if title_elem:
                title = title_elem.get_text().strip()
                title = re.sub(r'[|_-].*', '', title).strip()
        
        return title
    
    def _extract_episodes(self, soup: BeautifulSoup) -> List[Dict]:
        """提取分集信息"""
        episodes = []
        
        # 查找分集列表
        movurl_div = soup.find('div', class_='movurl')
        if not movurl_div:
            # 尝试其他选择器
            movurl_div = soup.find('div', id='main0')
        
        if not movurl_div:
            # 在整个页面中查找分集链接
            links = soup.find_all('a', href=re.compile(r'/v/\d+-\d+\.html'))
        else:
            links = movurl_div.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '').strip()
            title = link.get_text().strip()
            
            # 验证链接格式
            if href and re.match(r'/v/\d+-\d+\.html', href):
                full_url = urljoin(self.base_url, href)
                
                # 提取集数
                episode_match = re.search(r'-(\d+)\.html', href)
                episode_num = int(episode_match.group(1)) if episode_match else 0
                
                episodes.append({
                    'episode': episode_num,
                    'title': title,
                    'url': full_url,
                    'relative_url': href
                })
        
        # 按集数排序
        episodes.sort(key=lambda x: x['episode'])
        return episodes

def get_anime_episodes(anime_url: str) -> Dict:
    """获取动漫分集的API接口函数
    
    Args:
        anime_url: 动漫详情页URL
        
    Returns:
        包含分集信息的响应字典
    """
    crawler = EpisodesCrawler()
    
    try:
        episodes = crawler.crawl_episodes(anime_url)
        
        # 提取动漫标题
        anime_title = episodes[0]['anime_title'] if episodes else "未知动漫"
        
        return {
            'success': True,
            'anime_title': anime_title,
            'anime_url': anime_url,
            'total_episodes': len(episodes),
            'data': episodes,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'anime_url': anime_url,
            'total_episodes': 0,
            'data': [],
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # 从命令行参数获取动漫ID
    import sys
    if len(sys.argv) != 2:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python crawler_episodes.py <anime_id>'
        }))
        sys.exit(1)
    
    anime_id = sys.argv[1]
    
    # 构建完整的动漫URL
    if anime_id.startswith('show/'):
        anime_url = f"http://www.iyinghua.com/{anime_id}"
    else:
        anime_url = f"http://www.iyinghua.com/show/{anime_id}.html"
    
    result = get_anime_episodes(anime_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))