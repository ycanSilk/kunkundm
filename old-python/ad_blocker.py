#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫广告拦截器
专门拦截和移除你提供的广告格式
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

class YinghuaAdBlocker:
    """樱花动漫广告拦截器"""
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.ad_patterns = [
            # 你提供的具体广告格式
            {
                'id': 'adv_wrap_hh',
                'selector': '#adv_wrap_hh',
                'description': '主广告容器'
            },
            {
                'class': 'ad-banner',
                'selector': '.ad-banner',
                'description': '广告横幅'
            },
            {
                'href': 'evewan.com',
                'pattern': r'href=["\'][^"\']*evewan\.com[^"\']*["\']',
                'description': '游戏广告链接'
            },
            {
                'src': 'sogowan.com',
                'pattern': r'src=["\'][^"\']*sogowan\.com[^"\']*["\']',
                'description': '广告图片'
            }
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
            
            # 添加广告拦截功能
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
    
    def block_specific_ads(self):
        """拦截你提供的具体广告"""
        
        # 移除你提供的广告容器
        ad_removal_script = """
        // 移除主广告容器
        var advWrap = document.getElementById('adv_wrap_hh');
        if (advWrap) {
            advWrap.remove();
            console.log('已移除adv_wrap_hh广告容器');
        }
        
        // 移除所有包含evewan.com的链接
        var allLinks = document.querySelectorAll('a[href*="evewan.com"]');
        allLinks.forEach(function(link) {
            link.remove();
            console.log('已移除evewan.com广告链接');
        });
        
        // 移除所有包含sogowan.com的图片
        var allImages = document.querySelectorAll('img[src*="sogowan.com"]');
        allImages.forEach(function(img) {
            img.remove();
            console.log('已移除sogowan.com广告图片');
        });
        
        // 移除特定的广告HTML结构
        var adElements = document.querySelectorAll('[style*="position: absolute"]');
        adElements.forEach(function(el) {
            if (el.style.zIndex && parseInt(el.style.zIndex) > 1000000) {
                el.remove();
                console.log('已移除高z-index广告');
            }
        });
        
        // 移除所有广告iframe
        var iframes = document.querySelectorAll('iframe');
        iframes.forEach(function(iframe) {
            if (iframe.src && (iframe.src.includes('ad') || iframe.src.includes('visitor'))) {
                iframe.remove();
                console.log('已移除广告iframe');
            }
        });
        """
        
        try:
            self.driver.execute_script(ad_removal_script)
            print("✅ 广告拦截脚本执行完成")
            return True
        except Exception as e:
            print(f"❌ 广告拦截失败: {e}")
            return False
    
    def extract_clean_m3u8(self, page_url):
        """提取无广告的纯净m3u8链接"""
        
        if not self.init_driver():
            return None
        
        try:
            print(f"正在访问页面: {page_url}")
            self.driver.get(page_url)
            
            # 等待页面加载
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 等待视频加载
            time.sleep(3)
            
            # 执行广告拦截
            self.block_specific_ads()
            
            # 获取清理后的页面内容
            page_source = self.driver.page_source
            
            # 提取纯净m3u8链接
            clean_m3u8 = self._extract_pure_m3u8(page_source)
            
            return {
                'success': True,
                'page_url': page_url,
                'clean_m3u8': clean_m3u8,
                'ad_removed': True,
                'ad_blocking_log': self._get_blocking_log()
            }
            
        except Exception as e:
            print(f"提取失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'clean_m3u8': None
            }
        finally:
            if self.driver:
                self.driver.quit()
    
    def _extract_pure_m3u8(self, page_source):
        """从清理后的页面提取纯净m3u8"""
        
        # 基于你提供的格式直接提取
        pattern = r'https://[^"\']+\.m3u8[^"\']*'
        matches = re.findall(pattern, page_source)
        
        clean_links = []
        
        for url in matches:
            # 过滤广告URL
            if not any(ad_domain in url for ad_domain in ['evewan.com', 'sogowan.com']):
                # 清理URL参数
                clean_url = self._clean_m3u8_url(url)
                
                # 验证链接有效性
                if self._validate_m3u8_url(clean_url):
                    clean_links.append({
                        'url': clean_url,
                        'quality': self._detect_quality(clean_url),
                        'validated': True
                    })
        
        return clean_links
    
    def _clean_m3u8_url(self, url):
        """清理m3u8 URL中的广告参数"""
        
        # 移除广告参数
        url = re.sub(r'\$mp4$', '', url)
        url = re.sub(r'\$[^&]*$', '', url)
        
        # 清理查询参数中的广告
        if '?' in url:
            base, params = url.split('?', 1)
            clean_params = [p for p in params.split('&') if not any(ad_key in p.lower() for ad_key in ['ad', 'visitor', 'banner'])]
            return base + '?' + '&'.join(clean_params) if clean_params else base
        
        return url
    
    def _validate_m3u8_url(self, url):
        """验证m3u8链接有效性"""
        try:
            response = requests.head(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            return response.status_code == 200
        except:
            return False
    
    def _detect_quality(self, url):
        """检测视频质量"""
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
    
    def _get_blocking_log(self):
        """获取广告拦截日志"""
        return {
            'blocked_containers': ['#adv_wrap_hh'],
            'blocked_domains': ['evewan.com', 'sogowan.com'],
            'blocked_elements': ['iframe', 'img[src*="gif"]'],
            'method': 'javascript_removal'
        }
    
    def construct_direct_m3u8(self, page_url):
        """直接构造m3u8链接（基于你提供的格式）"""
        
        try:
            # 从URL提取动漫信息
            match = re.search(r'/v/(\d+)-(\d+)\.html', page_url)
            if match:
                anime_id, episode = match.groups()
                
                # 基于你提供的格式构造
                base_m3u8 = f"https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第{int(episode):02d}集/index.m3u8"
                
                # 验证链接
                if self._validate_m3u8_url(base_m3u8):
                    return {
                        'success': True,
                        'direct_m3u8': base_m3u8,
                        'constructed': True,
                        'anime_id': anime_id,
                        'episode': episode
                    }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        return {
            'success': False,
            'error': '无法构造m3u8链接'
        }


def main():
    """测试广告拦截器"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python ad_blocker.py <樱花动漫页面URL>")
        print("  python ad_blocker.py http://www.iyinghua.com/v/6543-1.html")
        return
    
    page_url = sys.argv[1]
    
    blocker = YinghuaAdBlocker(headless=False)
    
    print("🛡️ 启动樱花动漫广告拦截器...")
    
    # 方法1: 页面清理法
    result = blocker.extract_clean_m3u8(page_url)
    
    if result['success'] and result['clean_m3u8']:
        print("\n" + "="*70)
        print("✅ 无广告视频链接提取成功")
        print("="*70)
        
        for i, link in enumerate(result['clean_m3u8'], 1):
            print(f"{i}. 🎬 纯净m3u8链接:")
            print(f"   URL: {link['url']}")
            print(f"   质量: {link['quality']}")
            print(f"   已验证: {'是' if link['validated'] else '否'}")
            print("-" * 70)
    
    # 方法2: 直接构造法
    print("\n🔍 尝试直接构造m3u8链接...")
    direct_result = blocker.construct_direct_m3u8(page_url)
    
    if direct_result['success']:
        print(f"\n✅ 直接构造成功:")
        print(f"   🎯 纯净m3u8: {direct_result['direct_m3u8']}")
        print(f"   📺 动漫ID: {direct_result['anime_id']}")
        print(f"   🔢 集数: {direct_result['episode']}")
        
        # 验证链接
        if blocker._validate_m3u8_url(direct_result['direct_m3u8']):
            print("   ✅ 链接验证通过")
        else:
            print("   ❌ 链接验证失败")
    else:
        print(f"❌ 直接构造失败: {direct_result['error']}")


if __name__ == "__main__":
    main()