#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫视频URL解析器 - API版本
解析动漫页面URL为真实视频地址
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse
from typing import Dict, Optional
from datetime import datetime

class VideoCrawler:
    """视频URL解析爬虫类"""
    
    def __init__(self, base_url: str = "http://www.iyinghua.com"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
    
    def parse_video_url(self, page_url: str) -> Dict:
        """解析视频URL
        
        Args:
            page_url: 动漫播放页面URL
            
        Returns:
            视频信息字典
        """
        if not self._validate_url(page_url):
            raise ValueError("无效的页面URL")
        
        try:
            response = requests.get(page_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            return self._extract_video_url(response.text, page_url)
            
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
    
    def _extract_video_url(self, html_content: str, page_url: str) -> Dict:
        """从HTML内容中提取视频URL"""
        
        # 提取页面标题
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "未知视频"
        
        # 提取集数信息
        episode_match = re.search(r'第(\d+)集', title)
        current_episode = int(episode_match.group(1)) if episode_match else 1
        
        # 提取视频URL - 多种策略
        video_url = None
        
        # 策略1: 直接提取tup格式URL
        tup_pattern = r'["\'](https?://tup\.iyinghua\.com/\?vid=https?://[^"\']+\.m3u8[^"\']*)["\']'
        matches = re.findall(tup_pattern, html_content)
        if matches:
            video_url = matches[0]
        
        # 策略2: 提取vid参数并构造URL
        if not video_url:
            vid_pattern = r'["\']vid["\']:\s*["\'](https?://[^"\']+\.m3u8[^"\']*)["\']'
            vid_matches = re.findall(vid_pattern, html_content)
            if vid_matches:
                video_url = f"https://tup.iyinghua.com/?vid={vid_matches[0]}"
        
        # 策略3: 提取其他m3u8 URL
        if not video_url:
            m3u8_patterns = [
                r'["\'](https?://[^"\']*bf8bf\.com[^"\']*\.m3u8[^"\']*)["\']',
                r'["\'](https?://[^"\']*\.m3u8[^"\']*)["\']'
            ]
            for pattern in m3u8_patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    video_url = f"https://tup.iyinghua.com/?vid={matches[0]}"
                    break
        
        # 提取总集数
        total_episodes = 12  # 默认值
        episode_list_pattern = r'共(\d+)集'
        total_match = re.search(episode_list_pattern, html_content)
        if total_match:
            total_episodes = int(total_match.group(1))
        
        return {
            'video_url': video_url,
            'title': title,
            'current_episode': current_episode,
            'total_episodes': total_episodes,
            'source_url': page_url,
            'parsed_at': datetime.now().isoformat()
        }

def get_video_url(page_url: str) -> Dict:
    """获取视频URL的API接口函数
    
    Args:
        page_url: 动漫播放页面URL
        
    Returns:
        包含视频信息的响应字典
    """
    crawler = VideoCrawler()
    
    try:
        video_info = crawler.parse_video_url(page_url)
        
        return {
            'success': True,
            'data': video_info,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': {
                'video_url': None,
                'title': '解析失败',
                'current_episode': 1,
                'total_episodes': 1,
                'source_url': page_url,
                'parsed_at': datetime.now().isoformat()
            },
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # 测试函数
    test_url = "http://www.iyinghua.com/v/6543-1.html"
    result = get_video_url(test_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))