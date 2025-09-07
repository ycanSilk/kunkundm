#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫最新更新爬虫
爬取樱花动漫首页的最新更新内容
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from typing import List, Dict, Optional
from datetime import datetime

class LatestUpdateCrawler:
    def __init__(self):
        self.base_url = "http://www.iyinghua.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'http://www.iyinghua.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.latest_updates_selector = "body .area div .img ul li"
        
    def fetch_page(self, url: str) -> Optional[str]:
        """获取页面内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            print(f"获取页面失败: {e}")
            return None
    
    def parse_latest_updates(self, html: str) -> List[Dict[str, str]]:
        """解析最新更新内容"""
        soup = BeautifulSoup(html, 'html.parser')
        updates = []
        
        # 根据选择器查找最新更新内容
        update_items = soup.select(self.latest_updates_selector)
        
        for item in update_items:
            try:
                update_data = {}
                
                # 提取图片信息
                img_tag = item.find('img')
                if img_tag:
                    update_data['cover_image'] = img_tag.get('src', '')
                    update_data['title'] = img_tag.get('alt', '')
                
                # 提取链接信息
                link_tag = item.find('a')
                if link_tag:
                    href = link_tag.get('href', '')
                    if href.startswith('/'):
                        href = self.base_url + href
                    update_data['detail_url'] = href
                    
                    # 提取标题（如果图片中没有）
                    if not update_data.get('title'):
                        update_data['title'] = link_tag.get('title', '') or link_tag.text.strip()
                
                # 提取更新信息
                info_spans = item.find_all('span')
                for span in info_spans:
                    span_text = span.text.strip()
                    if '更新至' in span_text:
                        update_data['episode_info'] = span_text
                    elif '类型：' in span_text:
                        update_data['anime_type'] = span_text.replace('类型：', '').strip()
                
                # 提取集数信息
                episode_match = re.search(r'更新至(\d+)集', str(item))
                if episode_match:
                    update_data['current_episode'] = int(episode_match.group(1))
                
                if update_data.get('title') and update_data.get('detail_url'):
                    updates.append(update_data)
                    
            except Exception as e:
                print(f"解析项目失败: {e}")
                continue
        
        return updates
    
    def crawl_latest_updates(self) -> Dict[str, any]:
        """爬取最新更新"""
        print("开始爬取樱花动漫最新更新...")
        
        html = self.fetch_page(self.base_url)
        if not html:
            return {
                'success': False,
                'error': '无法获取页面内容',
                'data': [],
                'timestamp': datetime.now().isoformat()
            }
        
        updates = self.parse_latest_updates(html)
        
        result = {
            'success': True,
            'total_count': len(updates),
            'data': updates,
            'timestamp': datetime.now().isoformat(),
            'source_url': self.base_url
        }
        
        return result
    
    def save_to_json(self, data: Dict[str, any], filename: str = None) -> str:
        """保存数据到JSON文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'latest_updates_{timestamp}.json'
        
        filepath = filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到: {filepath}")
            return filepath
        except Exception as e:
            print(f"保存文件失败: {e}")
            return None
    
    def print_summary(self, data: Dict[str, any]) -> None:
        """打印摘要信息"""
        if data['success']:
            print(f"\n✅ 爬取成功!")
            print(f"📊 总更新数量: {data['total_count']}")
            print(f"⏰ 爬取时间: {data['timestamp']}")
            
            if data['data']:
                print("\n📋 最新更新列表:")
                for i, item in enumerate(data['data'][:5], 1):
                    print(f"{i}. {item.get('title', '未知标题')}")
                    if 'episode_info' in item:
                        print(f"   📺 {item['episode_info']}")
                    if 'anime_type' in item:
                        print(f"   🏷️ 类型: {item['anime_type']}")
                    print(f"   🔗 {item.get('detail_url', '')}")
                    print()
        else:
            print(f"❌ 爬取失败: {data.get('error', '未知错误')}")

def main():
    """主函数"""
    crawler = LatestUpdateCrawler()
    
    try:
        # 爬取最新更新
        result = crawler.crawl_latest_updates()
        
        # 打印摘要
        crawler.print_summary(result)
        
        # 保存数据
        if result['success']:
            crawler.save_to_json(result)
        
        return result
        
    except Exception as e:
        print(f"爬虫执行失败: {e}")
        return {
            'success': False,
            'error': str(e),
            'data': [],
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    main()