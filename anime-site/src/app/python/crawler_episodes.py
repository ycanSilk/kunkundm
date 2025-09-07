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
            
            # 提取封面图片URL
            cover_image = self._extract_cover_image(soup)
            
            # 提取分集信息
            episodes = self._extract_episodes(soup)
            
            # 添加动漫标题和封面图片到每个分集
            for episode in episodes:
                episode['anime_title'] = anime_title
                episode['anime_url'] = anime_url
                episode['cover_image'] = cover_image
            
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
        
        # 方式1: 查找h1标签
        title_elem = soup.find('h1')
        if title_elem:
            title = title_elem.get_text().strip()
        else:
            # 方式2: 查找title标签
            title_elem = soup.find('title')
            if title_elem:
                title = title_elem.get_text().strip()
                title = re.sub(r'[|_-].*', '', title).strip()
        
        # 方式3: 查找thumb区域的图片alt属性
        if title == "未知动漫":
            thumb_div = soup.find('div', class_='thumb')
            if thumb_div:
                img = thumb_div.find('img')
                if img and img.get('alt'):
                    title = img['alt'].strip()
        
        return title

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """提取动漫描述"""
        description = ""
        
        # 查找动漫介绍区域
        info_div = soup.find('div', class_='info')
        if info_div:
            description = info_div.get_text().strip()
        else:
            # 备用方案：查找meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '').strip()
        
        return description

    def _extract_anime_details(self, soup: BeautifulSoup) -> Dict:
        """提取完整动漫信息"""
        details = {}
        
        # 提取评分
        score_elem = soup.find('div', class_='score')
        if score_elem:
            rating = score_elem.find('em')
            if rating:
                try:
                    details['rating'] = float(rating.get_text().replace('分', ''))
                except:
                    details['rating'] = 0.0
        else:
            details['rating'] = 0.0
        
        # 提取详细信息
        sinfo = soup.find('div', class_='sinfo')
        if sinfo:
            spans = sinfo.find_all('span')
            for span in spans:
                label = span.find('label')
                if label:
                    label_text = label.get_text()
                    content = span.get_text().replace(label_text, '').strip()
                    
                    if '上映' in label_text:
                        details['release_date'] = content
                    elif '地区' in label_text:
                        details['region'] = content
                    elif '类型' in label_text:
                        # 提取类型链接
                        type_links = span.find_all('a')
                        details['genres'] = [link.get_text().strip() for link in type_links]
                    elif '标签' in label_text:
                        # 提取标签链接
                        tag_links = span.find_all('a')
                        details['tags'] = [link.get_text().strip() for link in tag_links]
        
        # 提取状态信息
        if sinfo:
            status_p = sinfo.find('p')
            if status_p:
                details['status'] = status_p.get_text().strip()
        
        return details

    def _normalize_image_url(self, url: str) -> str:
        """标准化图片URL"""
        if not url:
            return ""
        
        if url.startswith('//'):
            return 'https:' + url
        elif url.startswith('/'):
            return urljoin(self.base_url, url)
        elif url.startswith('http'):
            return url
        return url

    def _extract_cover_image(self, soup: BeautifulSoup) -> str:
        """提取封面图片URL（基于实际HTML结构）"""
        # 优先查找class="thumb"中的图片
        thumb_div = soup.find('div', class_='thumb')
        if thumb_div:
            img = thumb_div.find('img')
            if img and img.get('src'):
                return self._normalize_image_url(img['src'])
        
        # 备用方案：查找动漫标题相关的图片
        anime_title = self._extract_anime_title(soup)
        if anime_title and anime_title != "未知动漫":
            img_with_alt = soup.find('img', {'alt': anime_title})
            if img_with_alt and img_with_alt.get('src'):
                return self._normalize_image_url(img_with_alt['src'])
        
        # 通用方案：查找页面中合适的图片
        img_tags = soup.find_all('img')
        for img in img_tags:
            src = img.get('src', '')
            if src and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                # 排除广告和小图标
                if not any(ad in src.lower() for ad in ['ad', 'banner', 'logo', 'icon']):
                    normalized = self._normalize_image_url(src)
                    if normalized and len(normalized) > 10:  # 确保是有效URL
                        return normalized
        
        return ''
    
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

    def _extract_real_video_url(self, episode_url: str) -> str:
        """提取真实视频播放地址"""
        try:
            response = requests.get(episode_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找视频源
            # 方式1: 查找video标签
            video_tags = soup.find_all('video')
            for video in video_tags:
                src = video.get('src') 
                if not src:
                    source = video.find('source')
                    if source:
                        src = source.get('src')
                if src:
                    return self._normalize_image_url(src)
            
            # 方式2: 查找iframe中的视频源
            iframes = soup.find_all('iframe')
            for iframe in iframes:
                src = iframe.get('src')
                if src and any(keyword in src.lower() for keyword in ['player', 'video', 'play']):
                    return src
            
            # 方式3: 查找JavaScript中的视频URL
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # 查找m3u8链接
                    m3u8_matches = re.findall(r'["\'](https?://[^"\']*\.m3u8[^"\']*)["\']', script.string)
                    if m3u8_matches:
                        return m3u8_matches[0]
                    
                    # 查找mp4链接
                    mp4_matches = re.findall(r'["\'](https?://[^"\']*\.mp4[^"\']*)["\']', script.string)
                    if mp4_matches:
                        return mp4_matches[0]
            
            # 方式4: 查找data-video属性
            video_divs = soup.find_all(attrs={'data-video': True})
            for div in video_divs:
                video_url = div.get('data-video')
                if video_url:
                    return self._normalize_image_url(video_url)
            
            return episode_url  # 返回原始页面URL作为备用
            
        except Exception as e:
            print(f"提取视频URL失败: {e}")
            return episode_url

    def crawl_complete_anime_info(self, anime_url: str) -> Dict:
        """爬取完整动漫信息"""
        if not self._validate_url(anime_url):
            raise ValueError("无效的动漫页面URL")
        
        try:
            response = requests.get(anime_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取基础信息
            anime_title = self._extract_anime_title(soup)
            cover_image = self._extract_cover_image(soup)
            description = self._extract_description(soup)
            
            # 提取详细信息
            anime_details = self._extract_anime_details(soup)
            
            # 提取分集信息
            episodes = self._extract_episodes(soup)
            
            # 为每个分集提取真实视频URL
            for episode in episodes:
                episode['video_url'] = self._extract_real_video_url(episode['url'])
                episode['anime_title'] = anime_title
                episode['cover_image'] = cover_image
            
            return {
                'success': True,
                'anime_info': {
                    'title': anime_title,
                    'cover_image': cover_image,
                    'description': description,
                    **anime_details
                },
                'episodes': episodes,
                'total_episodes': len(episodes),
                'crawl_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'anime_url': anime_url,
                'total_episodes': 0,
                'episodes': [],
                'crawl_time': datetime.now().isoformat()
            }

def get_anime_episodes(anime_url: str) -> Dict:
    """获取动漫分集的API接口函数（兼容旧接口）"""
    crawler = EpisodesCrawler()
    return crawler.crawl_complete_anime_info(anime_url)

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
    # 强制使用UTF-8编码输出
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))