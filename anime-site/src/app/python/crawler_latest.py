#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫最新更新爬虫 - API版本
爬取首页最新更新的动漫内容
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import os
from typing import List, Dict, Optional
from datetime import datetime

class LatestCrawler:
    """最新更新爬虫类"""
    
    def __init__(self, base_url: str = "http://www.iyinghua.com"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': base_url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
        }
        self.latest_updates_selector = ".area .img ul li, .news-list li, .update-list li"
    
    def crawl_latest_updates(self, limit: int = 50) -> List[Dict]:
        """爬取最新更新内容
        
        Args:
            limit: 最大返回结果数
            
        Returns:
            最新更新动漫列表
        """
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            return self._parse_latest_updates(response.text, limit)
            
        except requests.RequestException as e:
            raise Exception(f"获取页面失败: {str(e)}")
    
    def _parse_latest_updates(self, html: str, limit: int) -> List[Dict]:
        """解析最新更新内容"""
        soup = BeautifulSoup(html, 'html.parser')
        updates = []
        
        # 查找所有可能的更新区域
        update_selectors = [
            '.area .img ul li',
            '.news-list li',
            '.update-list li',
            '.anime-list li',
            '.video-list li'
        ]
        
        update_items = []
        for selector in update_selectors:
            items = soup.select(selector)
            if items:
                update_items.extend(items)
                break
        
        # 如果没有找到，尝试更通用的选择器
        if not update_items:
            update_items = soup.find_all('li', class_=['anime-item', 'video-item', 'list-item'])
        
        # 如果还是找不到，尝试查找所有li中的动漫内容
        if not update_items:
            all_lis = soup.find_all('li')
            for li in all_lis:
                if li.find('img') and li.find('a'):
                    update_items.append(li)
        
        # 处理找到的所有项目
        for item in update_items[:limit]:
            try:
                update_data = {}
                
                # 提取图片信息
                img_tag = item.find('img')
                if img_tag:
                    update_data['cover_image'] = img_tag.get('src', '')
                    update_data['title'] = img_tag.get('alt', '')
                
                # 提取链接信息
                link_tag = item.find('a')
                if not link_tag:
                    link_tag = item.find('a', href=True)
                
                if link_tag:
                    href = link_tag.get('href', '')
                    if href.startswith('/'):
                        href = self.base_url + href
                    elif href.startswith('//'):
                        href = 'https:' + href
                    elif not href.startswith('http'):
                        href = self.base_url + '/' + href.lstrip('/')
                    update_data['detail_url'] = href
                    
                    # 提取标题（如果图片中没有）
                    if not update_data.get('title'):
                        title = link_tag.get('title', '') or link_tag.text.strip()
                        update_data['title'] = title.strip()
                
                # 提取更新信息
                info_spans = item.find_all('span')
                for span in info_spans:
                    span_text = span.text.strip()
                    if '更新至' in span_text:
                        update_data['episode_info'] = span_text
                    elif '集' in span_text and re.search(r'\d+', span_text):
                        update_data['episode_info'] = span_text
                    elif '类型：' in span_text:
                        update_data['anime_type'] = span_text.replace('类型：', '').strip()
                
                # 从文本中提取集数信息
                text_content = item.get_text()
                episode_match = re.search(r'更新至(\d+)集', text_content)
                if episode_match:
                    update_data['current_episode'] = int(episode_match.group(1))
                else:
                    # 尝试其他格式
                    episode_match = re.search(r'(\d+)集', text_content)
                    if episode_match:
                        update_data['current_episode'] = int(episode_match.group(1))
                
                # 清理和验证数据
                if update_data.get('title') and update_data.get('detail_url'):
                    # 确保图片URL完整
                    if update_data['cover_image']:
                        if update_data['cover_image'].startswith('//'):
                            update_data['cover_image'] = 'https:' + update_data['cover_image']
                        elif update_data['cover_image'].startswith('/'):
                            update_data['cover_image'] = self.base_url + update_data['cover_image']
                        elif not update_data['cover_image'].startswith('http'):
                            update_data['cover_image'] = self.base_url + '/' + update_data['cover_image'].lstrip('/')
                    
                    # 清理标题
                    update_data['title'] = update_data['title'].strip()
                    if update_data['title']:
                        updates.append(update_data)
                    
            except Exception as e:
                continue
        
        return updates

def get_latest_updates(limit: int = 50) -> Dict:
    """获取最新更新的API接口函数
    
    Args:
        limit: 最大返回结果数
        
    Returns:
        包含最新更新信息的响应字典
    """
    crawler = LatestCrawler()
    
    try:
        updates = crawler.crawl_latest_updates(limit)
        
        result = {
            'success': True,
            'total_count': len(updates),
            'data': updates,
            'timestamp': datetime.now().isoformat(),
            'source_url': crawler.base_url
        }
        
        # 保存为JSON文件
        try:
            # 确保data目录存在
            data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            # 固定文件名
            filepath = os.path.join(data_dir, 'latest_updates.json')
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            result['file_path'] = filepath
            
        except Exception as e:
            result['file_save_error'] = str(e)
        
        return result
        
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
    import sys
    limit = 50  # 默认获取50条
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            limit = 50
    
    result = get_latest_updates(limit=limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))