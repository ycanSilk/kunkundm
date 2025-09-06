#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫分集URL爬虫 - 命令行版本
支持批量爬取和多种输出格式
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import argparse
import sys
import os
from urllib.parse import urljoin, urlparse
from datetime import datetime

class AnimeEpisodeCrawler:
    def __init__(self, base_url="http://www.iyinghua.com"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
    def validate_url(self, url):
        """验证URL格式"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            if 'iyinghua.com' not in parsed.netloc:
                return False
            if not parsed.path.startswith('/show/'):
                return False
            return True
        except:
            return False
            
    def extract_anime_info(self, soup):
        """提取动漫基本信息"""
        title = "未知动漫"
        try:
            # 尝试多种方式提取标题
            title_elem = soup.find('h1')
            if title_elem:
                title = title_elem.get_text().strip()
            else:
                title_elem = soup.find('title')
                if title_elem:
                    title = title_elem.get_text().strip()
                    title = re.sub(r'[|_-].*', '', title).strip()
        except:
            pass
        return title
        
    def extract_episodes(self, soup):
        """提取分集信息"""
        episodes = []
        
        # 策略1: 查找标准分集列表
        movurl_div = soup.find('div', class_='movurl')
        if movurl_div:
            links = movurl_div.find_all('a', href=True)
        else:
            # 策略2: 广泛搜索所有可能的链接
            links = soup.find_all('a', href=re.compile(r'/v/\d+-\d+\.html'))
            
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
        
    def crawl_single_anime(self, url):
        """爬取单个动漫的分集信息"""
        print(f"🚀 开始爬取: {url}")
        
        if not self.validate_url(url):
            print("❌ 无效的动漫页面URL")
            return None
            
        try:
            print("🌐 发送请求...")
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            print(f"✅ 获取页面成功 ({len(response.text)} 字符)")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            anime_title = self.extract_anime_info(soup)
            episodes = self.extract_episodes(soup)
            
            if not episodes:
                print("⚠️ 未找到分集信息")
                return None
                
            result = {
                "anime_name": anime_title,
                "total_episodes": len(episodes),
                "source_url": url,
                "base_url": self.base_url,
                "crawl_time": datetime.now().isoformat(),
                "episodes": episodes
            }
            
            print(f"✅ 爬取完成！共找到 {len(episodes)} 集")
            return result
            
        except requests.RequestException as e:
            print(f"❌ 网络请求失败: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ 爬取失败: {str(e)}")
            return None
            
    def crawl_batch(self, urls):
        """批量爬取"""
        results = []
        for url in urls:
            result = self.crawl_single_anime(url.strip())
            if result:
                results.append(result)
        return results
        
    def export_data(self, data, filename, format_type='json'):
        """导出数据"""
        try:
            if format_type == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    
            elif format_type == 'txt':
                if isinstance(data, list):
                    # 批量结果
                    with open(filename, 'w', encoding='utf-8') as f:
                        for item in data:
                            f.write(f"🌸 {item['anime_name']}\n")
                            f.write(f"总集数: {item['total_episodes']}\n")
                            f.write(f"页面URL: {item['source_url']}\n")
                            f.write("=" * 50 + "\n")
                            for ep in item['episodes']:
                                f.write(f"第{ep['episode']:02d}集: {ep['url']}\n")
                            f.write("\n")
                else:
                    # 单个结果
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"🌸 {data['anime_name']}\n")
                        f.write(f"总集数: {data['total_episodes']}\n")
                        f.write(f"页面URL: {data['source_url']}\n")
                        f.write("=" * 50 + "\n")
                        for ep in data['episodes']:
                            f.write(f"第{ep['episode']:02d}集: {ep['url']}\n")
                            
            elif format_type == 'csv':
                import csv
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['动漫名称', '集数', '标题', '完整URL', '相对URL'])
                    
                    if isinstance(data, list):
                        for item in data:
                            for ep in item['episodes']:
                                writer.writerow([
                                    item['anime_name'],
                                    ep['episode'],
                                    ep['title'],
                                    ep['url'],
                                    ep['relative_url']
                                ])
                    else:
                        for ep in data['episodes']:
                            writer.writerow([
                                data['anime_name'],
                                ep['episode'],
                                ep['title'],
                                ep['url'],
                                ep['relative_url']
                            ])
                            
            print(f"✅ 数据已导出到: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ 导出失败: {str(e)}")
            return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='樱花动漫分集URL爬虫')
    parser.add_argument('url', nargs='?', help='动漫详情页URL')
    parser.add_argument('-f', '--file', help='从文件读取URL列表')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('-t', '--format', choices=['json', 'txt', 'csv'], default='json', help='输出格式')
    parser.add_argument('--base-url', default='http://www.iyinghua.com', help='基础URL')
    
    args = parser.parse_args()
    
    if not args.url and not args.file:
        print("❌ 请提供URL或使用-f参数指定文件")
        print("示例:")
        print("  python anime_episode_crawler.py http://www.iyinghua.com/show/6556.html")
        print("  python anime_episode_crawler.py -f urls.txt -o results.json")
        return
        
    crawler = AnimeEpisodeCrawler(args.base_url)
    
    # 获取URL列表
    urls = []
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ 文件未找到: {args.file}")
            return
    else:
        urls = [args.url]
        
    # 爬取数据
    if len(urls) == 1:
        data = crawler.crawl_single_anime(urls[0])
    else:
        data = crawler.crawl_batch(urls)
        
    if not data:
        print("❌ 未获取到任何数据")
        return
        
    # 导出数据
    if args.output:
        filename = args.output
    else:
        if len(urls) == 1:
            # 单个结果
            anime_name = data['anime_name'] if isinstance(data, dict) else data[0]['anime_name']
            filename = f"{anime_name}_episodes.{args.format}"
        else:
            # 批量结果
            filename = f"batch_episodes.{args.format}"
            
    crawler.export_data(data, filename, args.format)

if __name__ == "__main__":
    main()