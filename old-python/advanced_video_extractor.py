#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级樱花动漫视频链接提取器
支持加密视频源解析和多种播放格式
"""

import requests
import re
import json
import base64
import time
import hashlib
from urllib.parse import urljoin, urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import subprocess
import os

class AdvancedYinghuaExtractor:
    """高级樱花动漫视频提取器"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'http://www.iyinghua.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
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
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"初始化驱动失败: {e}")
            return False
    
    def extract_real_video_links(self, page_url):
        """
        提取真实视频链接（包括加密源）
        
        Args:
            page_url: 樱花动漫播放页面URL
            
        Returns:
            dict: 完整的视频信息
        """
        if not self.init_driver():
            return None
        
        try:
            print(f"开始提取: {page_url}")
            self.driver.get(page_url)
            
            # 等待播放器加载
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            
            # 等待额外时间让动态内容加载
            time.sleep(3)
            
            # 获取页面源代码
            page_source = self.driver.page_source
            
            # 提取视频信息
            video_data = self._extract_video_data(page_url)
            
            # 提取所有可能的视频源
            video_sources = self._extract_all_sources(page_source)
            
            # 提取播放配置
            player_config = self._extract_player_config(page_source)
            
            # 验证链接有效性
            valid_sources = self._validate_sources(video_sources)
            
            return {
                'success': True,
                'video_info': video_data,
                'sources': valid_sources,
                'player_config': player_config,
                'download_options': self._generate_download_options(valid_sources)
            }
            
        except Exception as e:
            print(f"提取失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'video_info': {},
                'sources': []
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def _extract_video_data(self, page_url):
        """提取视频元数据"""
        data = {}
        
        try:
            # 获取页面标题
            data['title'] = self.driver.title
            
            # 提取动漫信息
            parsed_url = urlparse(page_url)
            path_parts = parsed_url.path.split('/')
            
            if len(path_parts) >= 3:
                anime_info = path_parts[2].replace('.html', '')
                if '-' in anime_info:
                    anime_id, episode = anime_info.split('-')
                    data['anime_id'] = anime_id
                    data['episode'] = episode
            
            # 获取页面描述
            meta_desc = self.driver.find_elements(By.CSS_SELECTOR, "meta[name='description']")
            if meta_desc:
                data['description'] = meta_desc[0].get_attribute('content')
            
            # 提取视频时长
            video_element = self.driver.find_element(By.TAG_NAME, 'video')
            if video_element:
                duration = video_element.get_attribute('duration')
                if duration:
                    data['duration'] = float(duration)
        
        except Exception as e:
            print(f"提取视频数据失败: {e}")
        
        return data
    
    def _extract_all_sources(self, page_source):
        """提取所有视频源"""
        sources = []
        
        try:
            # 方法1: 直接查找video标签的src
            video_pattern = r'<video[^>]*src=["\']([^"\']+)["\'][^>]*>'
            video_src = re.findall(video_pattern, page_source)
            for src in video_src:
                sources.append({
                    'type': 'direct',
                    'url': src,
                    'quality': 'original',
                    'method': 'video_tag'
                })
            
            # 方法2: 查找source标签
            source_pattern = r'<source[^>]*src=["\']([^"\']+)["\'][^>]*type=["\']([^"\']+)["\'][^>]*>'
            source_matches = re.findall(source_pattern, page_source)
            for url, mime_type in source_matches:
                sources.append({
                    'type': mime_type.split('/')[-1],
                    'url': url,
                    'quality': self._detect_quality_from_url(url),
                    'method': 'source_tag'
                })
            
            # 方法3: 查找m3u8链接
            m3u8_pattern = r'https?://[^"\']+\.m3u8[^"\']*'
            m3u8_urls = re.findall(m3u8_pattern, page_source)
            for url in m3u8_urls:
                sources.append({
                    'type': 'm3u8',
                    'url': url,
                    'quality': self._detect_quality_from_url(url),
                    'method': 'm3u8_pattern'
                })
            
            # 方法4: 查找播放器配置
            player_configs = [
                r'player_aaaa\s*=\s*({[^}]+})',
                r'dpVideo\s*=\s*({[^}]+})',
                r'config\s*=\s*({[^}]+"url"[^}]+})',
                r'videoUrl\s*=\s*["\']([^"\']+)["\']',
                r'url\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']'
            ]
            
            for pattern in player_configs:
                matches = re.findall(pattern, page_source)
                for match in matches:
                    try:
                        if isinstance(match, str) and match.startswith('{'):
                            config = json.loads(match)
                            if 'url' in config:
                                sources.append({
                                    'type': 'config',
                                    'url': config['url'],
                                    'quality': config.get('quality', 'auto'),
                                    'method': 'player_config'
                                })
                        else:
                            sources.append({
                                'type': 'config',
                                'url': match,
                                'quality': 'auto',
                                'method': 'player_config'
                            })
                    except:
                        pass
            
            # 方法5: 查找加密配置
            encrypted_pattern = r'["\']([a-zA-Z0-9+/=]+)["\']'
            encrypted_matches = re.findall(encrypted_pattern, page_source)
            for encrypted in encrypted_matches:
                try:
                    decoded = base64.b64decode(encrypted).decode('utf-8')
                    if '.m3u8' in decoded:
                        sources.append({
                            'type': 'm3u8',
                            'url': decoded,
                            'quality': 'auto',
                            'method': 'base64_decoded'
                        })
                except:
                    pass
        
        except Exception as e:
            print(f"提取视频源失败: {e}")
        
        return sources
    
    def _extract_player_config(self, page_source):
        """提取播放器配置"""
        config = {}
        
        try:
            # 查找DPlayer配置
            dp_pattern = r'new\s+DPlayer\s*\(\s*({[^}]+})'
            dp_match = re.search(dp_pattern, page_source)
            if dp_match:
                try:
                    dp_config = json.loads(dp_match.group(1))
                    config['dplayer'] = dp_config
                except:
                    pass
            
            # 查找自定义播放器配置
            custom_patterns = [
                r'window\.playerConfig\s*=\s*({[^}]+})',
                r'playerOptions\s*=\s*({[^}]+})',
                r'videoOptions\s*=\s*({[^}]+})'
            ]
            
            for pattern in custom_patterns:
                match = re.search(pattern, page_source)
                if match:
                    try:
                        custom_config = json.loads(match.group(1))
                        config['custom'] = custom_config
                    except:
                        pass
        
        except Exception as e:
            print(f"提取播放器配置失败: {e}")
        
        return config
    
    def _detect_quality_from_url(self, url):
        """从URL检测视频质量"""
        url_lower = url.lower()
        
        quality_map = {
            '1080p': ['1080p', '1920x1080', 'fhd', 'fullhd'],
            '720p': ['720p', '1280x720', 'hd', 'high'],
            '480p': ['480p', '854x480', 'sd', 'standard'],
            '360p': ['360p', '640x360', 'ld', 'low'],
            '240p': ['240p', '426x240', 'vld', 'verylow']
        }
        
        for quality, keywords in quality_map.items():
            for keyword in keywords:
                if keyword in url_lower:
                    return quality
        
        return 'auto'
    
    def _validate_sources(self, sources):
        """验证视频源的有效性"""
        valid_sources = []
        
        for source in sources:
            try:
                url = source['url']
                if not url.startswith('http'):
                    continue
                
                # 发送HEAD请求验证
                response = self.session.head(url, timeout=5)
                if response.status_code == 200:
                    # 获取文件大小
                    file_size = response.headers.get('content-length')
                    if file_size:
                        source['file_size'] = int(file_size)
                    
                    # 获取内容类型
                    content_type = response.headers.get('content-type', '')
                    source['content_type'] = content_type
                    
                    valid_sources.append(source)
            except Exception as e:
                print(f"验证链接失败 {url}: {e}")
                continue
        
        return valid_sources
    
    def _generate_download_options(self, sources):
        """生成下载选项"""
        options = []
        
        # 按质量排序
        quality_order = ['1080p', '720p', '480p', '360p', '240p', 'auto']
        
        for quality in quality_order:
            for source in sources:
                if source['quality'] == quality:
                    options.append({
                        'quality': quality,
                        'url': source['url'],
                        'type': source['type'],
                        'filename': self._generate_filename(source)
                    })
        
        return options
    
    def _generate_filename(self, source):
        """生成文件名"""
        url = source['url']
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        if not filename:
            filename = f"video_{int(time.time())}.{source['type']}"
        
        return filename
    
    def download_with_ffmpeg(self, url, output_path, quality='best'):
        """使用ffmpeg下载视频"""
        try:
            cmd = [
                'ffmpeg',
                '-i', url,
                '-c', 'copy',
                '-bsf:a', 'aac_adtstoasc',
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "下载成功"
            else:
                return False, result.stderr
        
        except FileNotFoundError:
            return False, "未找到ffmpeg，请先安装ffmpeg"
        except Exception as e:
            return False, str(e)
    
    def extract_series_info(self, anime_url):
        """提取整部动漫的信息"""
        info = {
            'title': '',
            'episodes': [],
            'total_episodes': 0
        }
        
        try:
            if not self.init_driver():
                return info
            
            self.driver.get(anime_url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # 提取标题
            title_elem = soup.find('h1')
            if title_elem:
                info['title'] = title_elem.get_text(strip=True)
            
            # 提取所有集数
            episode_links = soup.find_all('a', href=re.compile(r'/v/\d+-\d+\.html'))
            
            for link in episode_links:
                href = link.get('href')
                if href:
                    episode_match = re.search(r'/v/(\d+)-(\d+)\.html', href)
                    if episode_match:
                        anime_id, episode_num = episode_match.groups()
                        episode_url = urljoin(anime_url, href)
                        
                        info['episodes'].append({
                            'episode': int(episode_num),
                            'url': episode_url,
                            'title': link.get_text(strip=True)
                        })
            
            info['total_episodes'] = len(info['episodes'])
            info['episodes'].sort(key=lambda x: x['episode'])
            
        except Exception as e:
            print(f"提取系列信息失败: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return info


def main():
    """测试函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("1. 提取单集: python advanced_video_extractor.py <单集URL>")
        print("2. 提取整剧: python advanced_video_extractor.py --series <动漫主页URL>")
        print("示例:")
        print("  python advanced_video_extractor.py http://www.iyinghua.com/v/6543-1.html")
        print("  python advanced_video_extractor.py --series http://www.iyinghua.com/v/6543/")
        return
    
    extractor = AdvancedYinghuaExtractor(headless=False)
    
    if sys.argv[1] == '--series':
        # 提取整剧信息
        series_url = sys.argv[2]
        info = extractor.extract_series_info(series_url)
        
        print(f"动漫: {info['title']}")
        print(f"总集数: {info['total_episodes']}")
        print("\n集数列表:")
        for ep in info['episodes']:
            print(f"第{ep['episode']}集: {ep['title']} - {ep['url']}")
    
    else:
        # 提取单集
        page_url = sys.argv[1]
        result = extractor.extract_real_video_links(page_url)
        
        if result['success']:
            print("="*60)
            print("视频信息:")
            print("="*60)
            for key, value in result['video_info'].items():
                print(f"{key}: {value}")
            
            print("\n" + "="*60)
            print("可用视频源:")
            print("="*60)
            
            for i, source in enumerate(result['sources'], 1):
                print(f"{i}. 类型: {source['type']}")
                print(f"   质量: {source['quality']}")
                print(f"   方法: {source['method']}")
                print(f"   URL: {source['url']}")
                
                if 'file_size' in source:
                    size_mb = source['file_size'] / (1024 * 1024)
                    print(f"   大小: {size_mb:.2f} MB")
                
                if 'content_type' in source:
                    print(f"   内容类型: {source['content_type']}")
                
                print("-" * 60)
            
            print("\n" + "="*60)
            print("下载选项:")
            print("="*60)
            for i, option in enumerate(result['download_options'], 1):
                print(f"{i}. {option['quality']} - {option['type']}")
                print(f"   URL: {option['url']}")
                print(f"   文件名: {option['filename']}")
                print("-" * 60)
        
        else:
            print("提取失败:", result.get('error', '未知错误'))


if __name__ == "__main__":
    main()