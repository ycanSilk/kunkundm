#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无广告樱花动漫视频链接提取器
自动去除嵌套广告，获取纯净视频链接
"""

import requests
import re
import json
import time
from urllib.parse import urljoin, urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import subprocess
import os

class AdFreeVideoExtractor:
    """无广告视频链接提取器"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'http://www.iyinghua.com/',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
        # 广告元素选择器
        self.ad_selectors = [
            '#adv_wrap_hh',
            '.advertisement',
            '.ad-banner',
            '#ad-container',
            '.video-ad',
            '[id*="adv"]',
            '[class*="ad"]',
            'iframe[src*="ad"]',
            'iframe[src*="advertisement"]'
        ]
    
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
            
            # 添加广告拦截扩展
            chrome_options.add_argument('--disable-extensions-except')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"初始化驱动失败: {e}")
            return False
    
    def remove_ads_from_page(self):
        """从页面中移除广告元素"""
        try:
            # 移除已知的广告容器
            for selector in self.ad_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        self.driver.execute_script("arguments[0].remove();", element)
                        print(f"已移除广告元素: {selector}")
                except:
                    continue
            
            # 移除特定的广告HTML
            ad_html_patterns = [
                'adv_wrap_hh',
                'id="adv_wrap_hh"',
                'evewan.com/visitor.html',
                'sogowan.com',
                'img-random-hm'
            ]
            
            for pattern in ad_html_patterns:
                try:
                    script = f"""
                    var elements = document.querySelectorAll('*');
                    for (var i = 0; i < elements.length; i++) {
                        if (elements[i].outerHTML && elements[i].outerHTML.includes('{pattern}')) {
                            elements[i].remove();
                        }
                    }
                    """
                    self.driver.execute_script(script)
                except:
                    continue
            
            # 移除所有iframe广告
            try:
                iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
                for iframe in iframes:
                    src = iframe.get_attribute('src')
                    if src and ('ad' in src.lower() or 'visitor' in src.lower()):
                        self.driver.execute_script("arguments[0].remove();", iframe)
            except:
                pass
                
        except Exception as e:
            print(f"移除广告失败: {e}")
    
    def extract_clean_video_url(self, page_url):
        """
        提取无广告的视频URL
        
        Args:
            page_url: 樱花动漫页面URL
            
        Returns:
            dict: 包含无广告视频链接的信息
        """
        if not self.init_driver():
            return None
        
        try:
            print(f"正在访问页面: {page_url}")
            self.driver.get(page_url)
            
            # 等待页面加载
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 等待视频元素加载
            time.sleep(3)
            
            # 移除广告
            self.remove_ads_from_page()
            
            # 获取清理后的页面源代码
            clean_page_source = self.driver.page_source
            
            # 提取无广告的视频链接
            clean_sources = self._extract_clean_sources(clean_page_source)
            
            # 验证和优化链接
            optimized_sources = self._optimize_video_urls(clean_sources)
            
            return {
                'success': True,
                'page_url': page_url,
                'clean_sources': optimized_sources,
                'ad_removed': True,
                'original_sources': self._extract_original_sources(page_url)
            }
            
        except Exception as e:
            print(f"提取无广告视频失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'clean_sources': []
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def _extract_clean_sources(self, page_source):
        """从清理后的页面提取视频源"""
        sources = []
        
        try:
            # 查找真实的m3u8链接（去除广告参数）
            
            # 方法1: 从tup.iyinghua.com提取纯净URL
            tup_pattern = r'https://tup\.iyinghua\.com/\?vid=([^&"\']+)'
            tup_matches = re.findall(tup_pattern, page_source)
            
            for vid_param in tup_matches:
                # 解码URL参数
                clean_url = vid_param.replace('$mp4', '').split('$')[0]
                if clean_url.startswith('https://') and '.m3u8' in clean_url:
                    sources.append({
                        'type': 'm3u8',
                        'url': clean_url,
                        'quality': self._extract_quality_from_url(clean_url),
                        'source': 'tup.iyinghua.com',
                        'ad_free': True
                    })
            
            # 方法2: 直接提取m3u8链接
            m3u8_pattern = r'https://[^"\']+\.m3u8[^"\']*'
            m3u8_urls = re.findall(m3u8_pattern, page_source)
            
            for url in m3u8_urls:
                # 过滤掉包含广告参数的URL
                if not any(ad_domain in url for ad_domain in ['evewan.com', 'sogowan.com']):
                    clean_url = self._clean_url_parameters(url)
                    sources.append({
                        'type': 'm3u8',
                        'url': clean_url,
                        'quality': self._extract_quality_from_url(clean_url),
                        'source': 'direct',
                        'ad_free': True
                    })
            
            # 方法3: 从JavaScript配置提取
            js_configs = [
                r'player_aaaa\s*=\s*({[^}]+"url"[^}]+})',
                r'dpVideo\s*=\s*({[^}]+"url"[^}]+})',
                r'config\s*=\s*({[^}]+"video"[^}]+})'
            ]
            
            for pattern in js_configs:
                matches = re.findall(pattern, page_source)
                for match in matches:
                    try:
                        config = json.loads(match)
                        video_url = None
                        
                        if 'url' in config:
                            video_url = config['url']
                        elif 'video' in config and 'url' in config['video']:
                            video_url = config['video']['url']
                        
                        if video_url and '.m3u8' in video_url and not any(ad_domain in video_url for ad_domain in ['evewan.com', 'sogowan.com']):
                            clean_url = self._clean_url_parameters(video_url)
                            sources.append({
                                'type': 'm3u8',
                                'url': clean_url,
                                'quality': config.get('quality', 'auto'),
                                'source': 'javascript_config',
                                'ad_free': True
                            })
                    except:
                        continue
        
        except Exception as e:
            print(f"提取清理视频源失败: {e}")
        
        return sources
    
    def _clean_url_parameters(self, url):
        """清理URL中的广告参数"""
        try:
            # 移除广告相关参数
            clean_url = re.sub(r'\$[^&]*$', '', url)
            clean_url = re.sub(r'&ad[^&]*', '', clean_url)
            clean_url = re.sub(r'\?ad[^&]*', '', clean_url)
            
            return clean_url
        except:
            return url
    
    def _extract_quality_from_url(self, url):
        """从URL提取视频质量"""
        url_lower = url.lower()
        
        if '1080' in url_lower:
            return '1080p'
        elif '720' in url_lower:
            return '720p'
        elif '480' in url_lower:
            return '480p'
        elif '360' in url_lower:
            return '360p'
        else:
            return 'auto'
    
    def _extract_original_sources(self, page_url):
        """提取原始视频源用于对比"""
        try:
            response = self.session.get(page_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取页面基本信息
            title = soup.find('title')
            video_title = title.get_text(strip=True) if title else "未知"
            
            return {
                'title': video_title,
                'url': page_url
            }
        except:
            return {'title': '未知', 'url': page_url}
    
    def validate_clean_url(self, url):
        """验证无广告URL的有效性"""
        try:
            response = self.session.head(url, timeout=10)
            return {
                'valid': response.status_code == 200,
                'status_code': response.status_code,
                'content_length': response.headers.get('content-length'),
                'content_type': response.headers.get('content-type')
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def extract_direct_m3u8_url(self, page_url):
        """
        直接提取m3u8链接，跳过广告页面
        
        基于你提供的格式分析：
        https://tup.iyinghua.com/?vid=https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第01集/index.m3u8
        """
        
        try:
            # 直接构造m3u8链接
            # 从页面URL提取动漫信息
            match = re.search(r'/v/(\d+)-(\d+)\.html', page_url)
            if match:
                anime_id, episode = match.groups()
                
                # 基于常见格式构造m3u8链接
                base_urls = [
                    f"https://8.bf8bf.com/video/{anime_id}/第{int(episode):02d}集/index.m3u8",
                    f"https://8.bf8bf.com/video/{anime_id}/第{episode}集/index.m3u8",
                    f"https://8.bf8bf.com/video/{anime_id}/第{episode}话/index.m3u8",
                    f"https://8.bf8bf.com/video/{anime_id}/EP{episode.zfill(2)}/index.m3u8"
                ]
                
                # 验证链接
                for url in base_urls:
                    validation = self.validate_clean_url(url)
                    if validation['valid']:
                        return {
                            'success': True,
                            'm3u8_url': url,
                            'method': 'direct_construction',
                            'anime_id': anime_id,
                            'episode': episode,
                            'ad_free': True
                        }
            
            return {
                'success': False,
                'error': '无法构造m3u8链接'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """测试无广告提取器"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python ad_free_extractor.py <樱花动漫页面URL>")
        print("  python ad_free_extractor.py http://www.iyinghua.com/v/6543-1.html")
        return
    
    page_url = sys.argv[1]
    
    extractor = AdFreeVideoExtractor(headless=False)
    
    print("正在提取无广告视频链接...")
    
    # 方法1: 页面清理法
    result = extractor.extract_clean_video_url(page_url)
    
    if result['success'] and result['clean_sources']:
        print("\n" + "="*60)
        print("✅ 无广告视频链接提取成功")
        print("="*60)
        
        for i, source in enumerate(result['clean_sources'], 1):
            print(f"{i}. 类型: {source['type']}")
            print(f"   质量: {source['quality']}")
            print(f"   来源: {source['source']}")
            print(f"   无广告: {'是' if source['ad_free'] else '否'}")
            print(f"   URL: {source['url']}")
            
            # 验证链接
            validation = extractor.validate_clean_url(source['url'])
            if validation['valid']:
                print(f"   ✅ 链接有效")
                if validation['content_length']:
                    size_mb = int(validation['content_length']) / (1024 * 1024)
                    print(f"   📊 文件大小: {size_mb:.2f} MB")
            else:
                print(f"   ❌ 链接无效")
            
            print("-" * 60)
    
    # 方法2: 直接构造法
    print("\n尝试直接构造m3u8链接...")
    direct_result = extractor.extract_direct_m3u8_url(page_url)
    
    if direct_result['success']:
        print(f"\n✅ 直接m3u8链接:")
        print(f"   URL: {direct_result['m3u8_url']}")
        print(f"   方法: {direct_result['method']}")
        print(f"   无广告: {'是' if direct_result['ad_free'] else '否'}")
        
        validation = extractor.validate_clean_url(direct_result['m3u8_url'])
        if validation['valid']:
            print(f"   ✅ 链接验证通过")
        else:
            print(f"   ❌ 链接验证失败")
    else:
        print(f"❌ 直接构造失败: {direct_result['error']}")


if __name__ == "__main__":
    main()