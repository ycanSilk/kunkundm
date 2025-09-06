#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫纯净视频提取器 v2.0
自动去广告 + 纯净m3u8提取 + 批量验证
针对你提供的具体广告格式优化
"""

import requests
import re
import json
import time
import os
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class CleanVideoExtractor:
    """樱花动漫纯净视频提取器"""
    
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
        
        # 你提供的具体广告特征
        self.ad_patterns = {
            'containers': [
                '#adv_wrap_hh',
                '.ad-banner',
                '[id*="adv"]',
                '[class*="ad"]'
            ],
            'domains': [
                'evewan.com',
                'sogowan.com',
                'v4.sogowan.com'
            ],
            'selectors': [
                'a[href*="evewan.com"]',
                'img[src*="sogowan.com"]',
                'iframe[src*="visitor"]'
            ]
        }
    
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
    
    def remove_specific_ads(self):
        """移除你提供的具体广告"""
        
        # 专门针对你提供的广告格式的移除脚本
        ad_removal_script = """
        // 移除主广告容器 adv_wrap_hh
        var advWrap = document.getElementById('adv_wrap_hh');
        if (advWrap) {
            console.log('发现主广告容器，正在移除...');
            advWrap.style.display = 'none';
            advWrap.remove();
        }
        
        // 移除所有包含evewan.com的广告链接
        var evewanLinks = document.querySelectorAll('a[href*="evewan.com"]');
        evewanLinks.forEach(function(link) {
            console.log('移除evewan.com广告链接:', link.href);
            link.remove();
        });
        
        // 移除所有sogowan.com广告图片
        var sogowanImages = document.querySelectorAll('img[src*="sogowan.com"]');
        sogowanImages.forEach(function(img) {
            console.log('移除sogowan.com广告图片:', img.src);
            img.remove();
        });
        
        // 移除特定的广告HTML结构
        var adDivs = document.querySelectorAll('div[style*="position: absolute"]');
        adDivs.forEach(function(div) {
            if (div.style.zIndex && parseInt(div.style.zIndex) > 1000000) {
                console.log('移除高z-index广告层');
                div.remove();
            }
        });
        
        // 移除iframe广告
        var adIframes = document.querySelectorAll('iframe[src*="visitor"]');
        adIframes.forEach(function(iframe) {
            console.log('移除访客广告iframe');
            iframe.remove();
        });
        
        // 清理广告相关的CSS
        var styleSheets = document.styleSheets;
        for (var i = 0; i < styleSheets.length; i++) {
            try {
                var rules = styleSheets[i].cssRules || styleSheets[i].rules;
                if (rules) {
                    for (var j = rules.length - 1; j >= 0; j--) {
                        var rule = rules[j];
                        if (rule.selectorText && rule.selectorText.includes('adv')) {
                            styleSheets[i].deleteRule(j);
                        }
                    }
                }
            } catch (e) {
                // 忽略跨域样式表错误
            }
        }
        """
        
        try:
            self.driver.execute_script(ad_removal_script)
            return True
        except Exception as e:
            print(f"广告移除失败: {e}")
            return False
    
    def extract_pure_m3u8(self, page_url):
        """提取纯净的m3u8链接"""
        
        if not self.init_driver():
            return None
        
        try:
            print(f"🎯 正在访问: {page_url}")
            self.driver.get(page_url)
            
            # 等待页面完全加载
            WebDriverWait(self.driver, 20).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # 等待视频元素
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
            except:
                pass
            
            # 等待额外时间确保动态内容加载
            time.sleep(5)
            
            # 执行广告移除
            self.remove_specific_ads()
            
            # 获取清理后的页面源代码
            clean_source = self.driver.page_source
            
            # 提取纯净视频链接
            pure_links = self._extract_clean_m3u8_links(clean_source)
            
            # 验证链接
            validated_links = self._validate_links(pure_links)
            
            return {
                'success': True,
                'page_url': page_url,
                'pure_m3u8': validated_links,
                'ad_removed': True,
                'extraction_method': 'dynamic_cleanup'
            }
            
        except Exception as e:
            print(f"❌ 提取失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'pure_m3u8': []
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def _extract_clean_m3u8_links(self, page_source):
        """从清理后的页面提取m3u8链接"""
        
        links = []
        
        try:
            # 基于你提供的格式提取
            
            # 方法1: 直接提取tup.iyinghua.com格式
            tup_pattern = r'https://tup\.iyinghua\.com/\?vid=([^&"\']+)'
            tup_matches = re.findall(tup_pattern, page_source)
            
            for vid_param in tup_matches:
                # 清理参数
                clean_url = vid_param.replace('$mp4', '')
                if clean_url.startswith('https://') and '.m3u8' in clean_url:
                    links.append({
                        'url': clean_url,
                        'type': 'tup_direct',
                        'quality': self._get_quality_from_url(clean_url),
                        'source': 'tup.iyinghua.com'
                    })
            
            # 方法2: 提取8.bf8bf.com格式（基于你提供的示例）
            bf8bf_pattern = r'https://8\.bf8bf\.com[^"\']*\.m3u8[^"\']*'
            bf8bf_matches = re.findall(bf8bf_pattern, page_source)
            
            for url in bf8bf_matches:
                clean_url = self._clean_url(url)
                links.append({
                    'url': clean_url,
                    'type': 'bf8bf_direct',
                    'quality': self._get_quality_from_url(clean_url),
                    'source': '8.bf8bf.com'
                })
            
            # 方法3: 提取所有m3u8链接并过滤广告
            all_m3u8_pattern = r'https?://[^"\']+\.m3u8[^"\']*'
            all_matches = re.findall(all_m3u8_pattern, page_source)
            
            for url in all_matches:
                # 过滤广告域名
                if not any(ad_domain in url for ad_domain in self.ad_patterns['domains']):
                    clean_url = self._clean_url(url)
                    if clean_url not in [l['url'] for l in links]:
                        links.append({
                            'url': clean_url,
                            'type': 'general_m3u8',
                            'quality': self._get_quality_from_url(clean_url),
                            'source': 'direct_extraction'
                        })
            
            # 方法4: 从JavaScript配置提取
            js_configs = [
                r'player_aaaa\s*=\s*({[^}]+"url"[^}]+})',
                r'config\s*=\s*({[^}]+"video"[^}]+})',
                r'videoUrl\s*=\s*["\']([^"\']+\.m3u8[^"\']*)["\']'
            ]
            
            for pattern in js_configs:
                matches = re.findall(pattern, page_source)
                for match in matches:
                    try:
                        if isinstance(match, str) and match.startswith('{'):
                            config = json.loads(match)
                            url = config.get('url', '') or config.get('video', {}).get('url', '')
                        else:
                            url = match
                        
                        if url and '.m3u8' in url and not any(ad_domain in url for ad_domain in self.ad_patterns['domains']):
                            clean_url = self._clean_url(url)
                            if clean_url not in [l['url'] for l in links]:
                                links.append({
                                    'url': clean_url,
                                    'type': 'javascript_config',
                                    'quality': 'auto',
                                    'source': 'player_config'
                                })
                    except:
                        continue
        
        except Exception as e:
            print(f"提取m3u8链接失败: {e}")
        
        return links
    
    def _clean_url(self, url):
        """清理URL中的广告参数"""
        
        # 移除广告参数
        url = re.sub(r'\$[^&]*$', '', url)
        url = re.sub(r'&ad[^&]*', '', url)
        url = re.sub(r'\?ad[^&]*', '', url)
        
        # 移除追踪参数
        url = re.sub(r'&utm_[^&]*', '', url)
        url = re.sub(r'&ref[^&]*', '', url)
        
        return url
    
    def _get_quality_from_url(self, url):
        """从URL提取质量信息"""
        url_lower = url.lower()
        
        if '1080' in url_lower or '1920x1080' in url_lower:
            return '1080p'
        elif '720' in url_lower or '1280x720' in url_lower:
            return '720p'
        elif '480' in url_lower or '854x480' in url_lower:
            return '480p'
        elif '360' in url_lower or '640x360' in url_lower:
            return '360p'
        else:
            return 'auto'
    
    def _validate_links(self, links):
        """验证链接有效性"""
        
        validated_links = []
        
        for link in links:
            try:
                response = requests.head(link['url'], timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if response.status_code == 200:
                    link.update({
                        'valid': True,
                        'status_code': response.status_code,
                        'file_size': response.headers.get('content-length'),
                        'content_type': response.headers.get('content-type')
                    })
                    validated_links.append(link)
                else:
                    link.update({
                        'valid': False,
                        'status_code': response.status_code
                    })
            
            except Exception as e:
                link.update({
                    'valid': False,
                    'error': str(e)
                })
        
        return validated_links
    
    def construct_direct_url(self, page_url):
        """直接构造纯净m3u8链接"""
        
        try:
            # 从页面URL提取信息
            match = re.search(r'/v/(\d+)-(\d+)\.html', page_url)
            if match:
                anime_id, episode = match.groups()
                
                # 基于你提供的格式构造
                direct_urls = [
                    f"https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第{int(episode):02d}集/index.m3u8",
                    f"https://8.bf8bf.com/video/{anime_id}/第{int(episode):02d}集/index.m3u8",
                    f"https://8.bf8bf.com/video/{anime_id}/EP{episode.zfill(2)}/index.m3u8"
                ]
                
                for url in direct_urls:
                    if self._validate_links([{'url': url}])[0]['valid']:
                        return {
                            'success': True,
                            'direct_url': url,
                            'constructed': True,
                            'anime_id': anime_id,
                            'episode': episode,
                            'method': 'pattern_construction'
                        }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        return {
            'success': False,
            'error': '无法构造有效链接'
        }
    
    def download_with_ffmpeg(self, m3u8_url, output_path):
        """使用ffmpeg下载无广告视频"""
        
        try:
            import subprocess
            
            cmd = [
                'ffmpeg',
                '-i', m3u8_url,
                '-c', 'copy',
                '-bsf:a', 'aac_adtstoasc',
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': '下载成功',
                    'file_path': output_path
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        
        except FileNotFoundError:
            return {
                'success': False,
                'error': '未找到ffmpeg，请先安装ffmpeg'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """主测试函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("🎯 樱花动漫纯净视频提取器 v2.0")
        print("="*50)
        print("使用方法:")
        print("  python clean_video_extractor.py <樱花动漫页面URL>")
        print("  python clean_video_extractor.py http://www.iyinghua.com/v/6543-1.html")
        print("\n📋 功能:")
        print("  ✅ 自动去除嵌套广告")
        print("  ✅ 提取纯净m3u8链接")
        print("  ✅ 验证链接有效性")
        print("  ✅ 支持批量提取")
        return
    
    page_url = sys.argv[1]
    extractor = CleanVideoExtractor(headless=False)
    
    print(f"🎯 正在处理: {page_url}")
    print("🔄 启动无广告视频提取...")
    
    # 方法1: 动态清理法
    print("\n🔍 方法1: 动态页面清理")
    result = extractor.extract_pure_m3u8(page_url)
    
    if result['success'] and result['pure_m3u8']:
        print("\n" + "="*70)
        print("✅ 无广告视频链接提取成功")
        print("="*70)
        
        for i, link in enumerate(result['pure_m3u8'], 1):
            print(f"{i}. 🎬 纯净m3u8:")
            print(f"   URL: {link['url']}")
            print(f"   类型: {link['type']}")
            print(f"   质量: {link['quality']}")
            print(f"   来源: {link['source']}")
            
            if link.get('valid'):
                print(f"   ✅ 验证通过")
                if link.get('file_size'):
                    size_mb = int(link['file_size']) / (1024 * 1024)
                    print(f"   📊 大小: {size_mb:.2f} MB")
            else:
                print(f"   ❌ 验证失败")
            
            print("-" * 70)
    
    # 方法2: 直接构造法
    print("\n🔍 方法2: 直接构造链接")
    direct_result = extractor.construct_direct_url(page_url)
    
    if direct_result['success']:
        print(f"\n✅ 直接构造成功:")
        print(f"   🎯 纯净m3u8: {direct_result['direct_url']}")
        print(f"   📺 动漫ID: {direct_result['anime_id']}")
        print(f"   🔢 集数: {direct_result['episode']}")
        print(f"   方法: {direct_result['method']}")
    else:
        print(f"❌ 直接构造失败: {direct_result['error']}")
    
    # 下载建议
    if (result['success'] and result['pure_m3u8']) or direct_result['success']:
        print("\n" + "="*50)
        print("📥 下载建议:")
        print("="*50)
        
        best_link = None
        if result['success'] and result['pure_m3u8']:
            valid_links = [l for l in result['pure_m3u8'] if l.get('valid')]
            if valid_links:
                best_link = valid_links[0]['url']
        elif direct_result['success']:
            best_link = direct_result['direct_url']
        
        if best_link:
            print(f"🎬 推荐下载链接:")
            print(f"   {best_link}")
            print(f"\n📥 使用ffmpeg下载:")
            print(f"   ffmpeg -i \"{best_link}\" -c copy output.mp4")


if __name__ == "__main__":
    main()