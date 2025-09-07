#!/usr/bin/env python3
"""
樱花动漫每日更新爬虫
爬取 http://www.iyinghua.com/ 的每日更新数据
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
import time
import re

class DailyUpdateCrawler:
    def __init__(self):
        self.base_url = "http://www.iyinghua.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
    def fetch_page(self, url):
        """获取页面内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.text
            else:
                print(f"获取页面失败，状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取页面时出错: {e}")
            return None
    
    def parse_daily_updates(self, html_content):
        """解析每日更新数据 - 按照指定选择器规则爬取"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 根据新的选择器规则定位区域
        # .area .side r .bg .tlist ul
        daily_update_section = soup.select_one('.area .side .r .bg')
        
        if not daily_update_section:
            print("未找到每日更新区域，尝试其他选择器...")
            # 尝试其他可能的选择器
            daily_update_section = soup.select_one('.side .bg')
            if not daily_update_section:
                daily_update_section = soup.find(class_='bg')
        
        if not daily_update_section:
            print("无法定位每日更新区域")
            return {}
        
        # 获取所有的tlist ul
        tlist_uls = daily_update_section.select('.tlist ul')
        
        if not tlist_uls:
            print("未找到tlist ul元素")
            return {}
        
        # 星期映射 - 对应7个ul
        week_days = [
            'monday',    # 第1个ul - 星期一
            'tuesday',   # 第2个ul - 星期二
            'wednesday', # 第3个ul - 星期三
            'thursday',  # 第4个ul - 星期四
            'friday',    # 第5个ul - 星期五
            'saturday',  # 第6个ul - 星期六
            'sunday'     # 第7个ul - 星期日
        ]
        
        week_data = {}
        
        # 遍历每个ul，最多7个
        for index, ul in enumerate(tlist_uls[:7]):
            if index >= len(week_days):
                break
                
            day_key = week_days[index]
            week_data[day_key] = []
            
            # 获取当前ul下的所有li
            li_elements = ul.find_all('li')
            
            for li in li_elements:
                # 查找li内的所有a标签
                a_tags = li.find_all('a')
                if not a_tags:
                    continue
                
                # 获取集数信息 - li span a (第一个a标签)
                episode_text = ""
                span = li.find('span')
                if span:
                    span_a = span.find('a')
                    if span_a:
                        episode_text = span_a.get_text().strip()
                
                # 获取动漫名称 - li a:nth-child(2) 或最后一个a标签
                # 根据HTML结构，动漫名称通常是最后一个a标签
                anime_a = a_tags[-1]  # 最后一个a标签是动漫名称
                title = anime_a.get_text().strip()
                href = anime_a.get('href', '')
                
                if not title or not href:
                    continue
                
                # 构建完整的URL
                full_url = href if href.startswith('http') else self.base_url + href
                
                # 构建动漫信息
                anime_info = {
                    'name': title,           # 动漫名称
                    'url': full_url,         # 详情页链接
                    'episode': episode_text  # 集数信息
                }
                
                week_data[day_key].append(anime_info)
        
        # 清理空的天
        week_data = {
            day: animes
            for day, animes in week_data.items()
            if animes
        }
        
        return week_data
    
    def extract_episode_from_title(self, title):
        """从标题中提取集数信息"""
        patterns = [
            r'第(\d+)集',
            r'(\d+)集',
            r'第(\d+)话',
            r'(\d+)话',
            r'第(\d+)期',
            r'第(\d+)季',
            r'(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title)
            if match:
                return match.group(1)
        return ''
    
    def save_data(self, data, filename=None):
        """保存数据到JSON文件 - 更新固定文件"""
        if filename is None:
            filename = "crawler_daily_update.json"
        
        # 确保输出目录存在 - 直接保存到 anime-site/data
        output_dir = os.path.join(os.path.dirname(__file__), '..','..','..', 'data')
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, filename)
        
        # 检查文件是否存在，如果存在则读取现有数据
        existing_data = {}
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = {}
        
        # 更新数据
        updated_data = {
            'updated_at': datetime.now().isoformat(),
            'source_url': self.base_url,
            'weekly_updates': data
        }
        
        # 写入更新后的数据
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已更新到: {file_path}")
        return file_path
    
    def run(self):
        """运行爬虫"""
        print("开始爬取每日更新数据...")
        
        # 获取页面内容
        html_content = self.fetch_page(self.base_url)
        if not html_content:
            return None
        
        # 解析数据
        daily_data = self.parse_daily_updates(html_content)
        
        if daily_data:
            # 保存数据
            file_path = self.save_data(daily_data)
            
            # 打印统计信息
            total_animes = sum(len(animes) for animes in daily_data.values())
            print(f"爬取完成! 共获取 {len(daily_data)} 天的数据，总计 {total_animes} 部动漫")
            
            for day, animes in daily_data.items():
                print(f"{day}: {len(animes)} 部")
            
            return file_path
        else:
            print("未能获取到有效的每日更新数据")
            return None

if __name__ == "__main__":
    crawler = DailyUpdateCrawler()
    crawler.run()