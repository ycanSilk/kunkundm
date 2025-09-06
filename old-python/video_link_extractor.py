#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫真实视频链接提取工具
专门用于从樱花动漫页面提取真实的m3u8视频链接
"""

import requests
import re
import json
import time
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import sys

class YinghuaVideoExtractor:
    """樱花动漫视频链接提取器"""
    
    def __init__(self, headless=True):
        """初始化提取器"""
        self.headless = headless
        self.driver = None
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'http://www.iyinghua.com/'
        })
    
    def init_driver(self):
        """初始化浏览器驱动"""
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            return True
        except Exception as e:
            print(f"初始化驱动失败: {e}")
            return False
    
    def extract_video_links(self, page_url):
        """
        从樱花动漫页面提取真实视频链接
        
        Args:
            page_url: 樱花动漫播放页面URL，如 http://www.iyinghua.com/v/6543-1.html
            
        Returns:
            dict: 包含视频信息的字典
        """
        if not self.init_driver():
            return None
        
        try:
            print(f"正在访问页面: {page_url}")
            self.driver.get(page_url)
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 获取页面源代码
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 提取视频信息
            video_info = self._extract_video_info(soup, page_url)
            
            # 提取真实视频链接
            video_links = self._extract_m3u8_links(page_source, page_url)
            
            return {
                'video_info': video_info,
                'video_links': video_links,
                'success': True
            }
            
        except Exception as e:
            print(f"提取视频链接失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'video_info': {},
                'video_links': []
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def _extract_video_info(self, soup, page_url):
        """提取视频基本信息"""
        info = {}
        
        try:
            # 提取标题
            title_elem = soup.find('h1')
            if title_elem:
                info['title'] = title_elem.get_text(strip=True)
            
            # 提取集数信息
            current_episode = re.search(r'-(\d+)\.html', page_url)
            if current_episode:
                info['current_episode'] = current_episode.group(1)
            
            # 提取动漫ID
            anime_id = re.search(r'/v/(\d+)-', page_url)
            if anime_id:
                info['anime_id'] = anime_id.group(1)
            
            # 尝试提取其他信息
            meta_info = soup.find('div', class_='info')
            if meta_info:
                info['description'] = meta_info.get_text(strip=True)
                
        except Exception as e:
            print(f"提取视频信息失败: {e}")
        
        return info
    
    def _extract_m3u8_links(self, page_source, page_url):
        """提取m3u8视频链接"""
        video_links = []
        
        try:
            # 方法1: 查找页面中的m3u8链接
            m3u8_pattern = r'https?://[^"\']+\.m3u8[^"\']*'
            m3u8_urls = re.findall(m3u8_pattern, page_source)
            
            if m3u8_urls:
                for url in m3u8_urls:
                    if 'index.m3u8' in url or '.m3u8' in url:
                        video_links.append({
                            'type': 'm3u8',
                            'url': url,
                            'quality': self._detect_quality(url),
                            'method': 'direct_m3u8'
                        })
            
            # 方法2: 查找iframe中的视频链接
            iframe_pattern = r'<iframe[^>]+src=["\']([^"\']+)["\'][^>]*>'
            iframes = re.findall(iframe_pattern, page_source)
            
            for iframe_src in iframes:
                if not iframe_src.startswith('http'):
                    iframe_src = urljoin(page_url, iframe_src)
                
                iframe_links = self._extract_from_iframe(iframe_src)
                video_links.extend(iframe_links)
            
            # 方法3: 查找JavaScript中的视频配置
            js_config_pattern = r'player_aaaa\s*=\s*({[^}]+})'
            js_match = re.search(js_config_pattern, page_source)
            if js_match:
                try:
                    config_str = js_match.group(1)
                    config = json.loads(config_str)
                    if 'url' in config:
                        video_links.append({
                            'type': 'm3u8',
                            'url': config['url'],
                            'quality': 'auto',
                            'method': 'js_config'
                        })
                except:
                    pass
            
            # 方法4: 查找DPlayer配置
            dp_config_pattern = r'dpVideo\s*=\s*({[^}]+})'
            dp_match = re.search(dp_config_pattern, page_source)
            if dp_match:
                try:
                    config_str = dp_match.group(1)
                    config = json.loads(config_str)
                    if 'video' in config and 'url' in config['video']:
                        video_links.append({
                            'type': 'mp4',
                            'url': config['video']['url'],
                            'quality': config['video'].get('quality', 'unknown'),
                            'method': 'dplayer_config'
                        })
                except:
                    pass
        
        except Exception as e:
            print(f"提取m3u8链接失败: {e}")
        
        return video_links
    
    def _extract_from_iframe(self, iframe_url):
        """从iframe中提取视频链接"""
        links = []
        
        try:
            response = self.session.get(iframe_url, timeout=10)
            content = response.text
            
            # 查找m3u8链接
            m3u8_pattern = r'https?://[^"\']+\.m3u8[^"\']*'
            m3u8_urls = re.findall(m3u8_pattern, content)
            
            for url in m3u8_urls:
                links.append({
                    'type': 'm3u8',
                    'url': url,
                    'quality': self._detect_quality(url),
                    'method': 'iframe_m3u8',
                    'source': iframe_url
                })
            
            # 查找mp4链接
            mp4_pattern = r'https?://[^"\']+\.mp4[^"\']*'
            mp4_urls = re.findall(mp4_pattern, content)
            
            for url in mp4_urls:
                links.append({
                    'type': 'mp4',
                    'url': url,
                    'quality': self._detect_quality(url),
                    'method': 'iframe_mp4',
                    'source': iframe_url
                })
                
        except Exception as e:
            print(f"从iframe提取失败: {e}")
        
        return links
    
    def _detect_quality(self, url):
        """检测视频质量"""
        url_lower = url.lower()
        
        if '1080p' in url_lower or '1920x1080' in url_lower:
            return '1080p'
        elif '720p' in url_lower or '1280x720' in url_lower:
            return '720p'
        elif '480p' in url_lower or '854x480' in url_lower:
            return '480p'
        elif '360p' in url_lower or '640x360' in url_lower:
            return '360p'
        else:
            return 'auto'
    
    def test_m3u8_url(self, m3u8_url):
        """测试m3u8链接是否有效"""
        try:
            response = self.session.head(m3u8_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_all_episodes(self, anime_id):
        """获取动漫的所有集数链接"""
        episodes = []
        
        try:
            # 构造动漫主页URL
            anime_url = f"http://www.iyinghua.com/v/{anime_id}/"
            
            response = self.session.get(anime_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有集数链接
            episode_links = soup.find_all('a', href=re.compile(rf'/v/{anime_id}-\d+\.html'))
            
            for link in episode_links:
                episode_num = re.search(rf'/v/{anime_id}-(\d+)\.html', link.get('href'))
                if episode_num:
                    episodes.append({
                        'episode': int(episode_num.group(1)),
                        'url': urljoin(anime_url, link.get('href')),
                        'title': link.get_text(strip=True)
                    })
            
            episodes.sort(key=lambda x: x['episode'])
            
        except Exception as e:
            print(f"获取集数列表失败: {e}")
        
        return episodes


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python video_link_extractor.py <樱花动漫页面URL>")
        print("示例: python video_link_extractor.py http://www.iyinghua.com/v/6543-1.html")
        return
    
    page_url = sys.argv[1]
    
    extractor = YinghuaVideoExtractor(headless=False)
    result = extractor.extract_video_links(page_url)
    
    if result and result['success']:
        print("\n" + "="*50)
        print("视频信息:")
        print("="*50)
        for key, value in result['video_info'].items():
            print(f"{key}: {value}")
        
        print("\n" + "="*50)
        print("视频链接:")
        print("="*50)
        for i, link in enumerate(result['video_links'], 1):
            print(f"{i}. 类型: {link['type']}")
            print(f"   质量: {link['quality']}")
            print(f"   方法: {link['method']}")
            print(f"   URL: {link['url']}")
            print("-" * 50)
    else:
        print("提取失败:", result.get('error', '未知错误'))


if __name__ == "__main__":
    main()