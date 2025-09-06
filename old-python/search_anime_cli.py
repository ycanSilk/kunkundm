#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫搜索爬虫 - 命令行版本
支持批量搜索和多种输出格式
"""

import requests
from bs4 import BeautifulSoup
import json
import argparse
import sys
import urllib.parse
from datetime import datetime
import re
import os

class AnimeSearchCLI:
    def __init__(self):
        self.base_url = "http://www.iyinghua.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def search_anime(self, keyword):
        """搜索动漫"""
        try:
            encoded_keyword = urllib.parse.quote(keyword)
            search_url = f"{self.base_url}/search/{encoded_keyword}/"
            
            print(f"🌸 正在搜索: {keyword}")
            print(f"🔗 URL: {search_url}")
            
            response = requests.get(search_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            return self.parse_search_results(response.text, keyword)
            
        except requests.RequestException as e:
            print(f"❌ 网络请求失败: {str(e)}")
            return []
        except Exception as e:
            print(f"❌ 搜索失败: {str(e)}")
            return []

    def parse_search_results(self, html_content, keyword):
        """解析搜索结果"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # 查找搜索结果列表
        lpic_div = soup.find('div', class_='lpic')
        if not lpic_div:
            print("⚠️ 未找到搜索结果")
            return results
            
        anime_items = lpic_div.find_all('li')
        
        print(f"📊 找到 {len(anime_items)} 个动漫")
        
        for index, item in enumerate(anime_items, 1):
            try:
                anime_data = {
                    'index': index,
                    'search_keyword': keyword,
                    'search_time': datetime.now().isoformat()
                }
                
                # 图片
                img_tag = item.find('img')
                if img_tag:
                    anime_data['image_url'] = img_tag.get('src', '')
                    anime_data['title_raw'] = img_tag.get('alt', '')
                
                # 标题和链接
                title_link = item.find('h2').find('a') if item.find('h2') else None
                if title_link:
                    anime_data['title'] = title_link.get_text(strip=True)
                    anime_data['detail_url'] = urllib.parse.urljoin(self.base_url, title_link.get('href', ''))
                    anime_data['detail_path'] = title_link.get('href', '')
                
                # 提取ID
                detail_path = anime_data.get('detail_path', '')
                id_match = re.search(r'/show/(\d+)\.html', detail_path)
                if id_match:
                    anime_data['anime_id'] = id_match.group(1)
                
                # 直接获取真实的集数标签内容 - 原样提取，不做任何判断
                spans = item.find_all('span')
                episodes_text = "未知"
                if spans:
                    # 直接获取第一个span的完整文本内容
                    episodes_text = spans[0].get_text(strip=True)
                anime_data['episodes_raw'] = episodes_text
                
                # 提取纯数字集数
                ep_match = re.search(r'(\d+)', anime_data['episodes_raw'])
                if ep_match:
                    anime_data['episodes_count'] = int(ep_match.group(1))
                else:
                    anime_data['episodes_count'] = None
                
                # 类型信息 - 基于实际HTML结构优化
                anime_data['genres'] = []
                anime_data['genres_str'] = ''
                
                spans = item.find_all('span')
                for span in spans:
                    text = span.get_text(strip=True)
                    if '类型：' in text:
                        type_links = span.find_all('a')
                        if type_links:
                            anime_data['genres'] = [a.get_text(strip=True) for a in type_links]
                        else:
                            # 处理没有a标签的情况，直接从文本提取
                            type_text = text.replace('类型：', '').strip()
                            # 按常见类型分割
                            types = []
                            common_types = ['搞笑', '冒险', '校园', '日常', '奇幻', '百合', '战斗', '热血', '科幻', '恋爱', '魔法', '治愈', '悬疑', '恐怖', '历史', '运动', '音乐', '校园', '日常']
                            for t in common_types:
                                if t in type_text:
                                    types.append(t)
                            if types:
                                anime_data['genres'] = types
                            else:
                                # 如果无法分割，将整个文本作为一个类型
                                anime_data['genres'] = [type_text] if type_text else []
                        
                        anime_data['genres_str'] = ' '.join(anime_data['genres'])
                        break
                
                # 描述
                desc_p = item.find('p')
                if desc_p:
                    anime_data['description'] = desc_p.get_text(strip=True)
                
                # 完整信息
                anime_data['source_url'] = f"{self.base_url}/search/{urllib.parse.quote(keyword)}/"
                anime_data['base_url'] = self.base_url
                
                results.append(anime_data)
                
                # 命令行输出
                print(f"\n🎭 [{index}] {anime_data.get('title', '未知标题')}")
                print(f"   📺 集数: {anime_data.get('episodes_raw', '未知')}")
                print(f"   🏷️  类型: {anime_data.get('genres_str', '未知')}")
                print(f"   🔗 详情: {anime_data.get('detail_url', '')}")
                if len(anime_data.get('description', '')) > 150:
                    print(f"   📝 简介: {anime_data['description'][:150]}...")
                else:
                    print(f"   📝 简介: {anime_data.get('description', '暂无简介')}")
                if anime_data.get('image_url'):
                    print(f"   🖼️ 图片: {anime_data['image_url']}")
                
            except Exception as e:
                print(f"⚠️ 解析第 {index} 个动漫失败: {str(e)}")
                continue
        
        return results

    def export_results(self, results, filename, format_type='json'):
        """导出结果"""
        try:
            if format_type == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                    
            elif format_type == 'txt':
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"🌸 樱花动漫搜索结果 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for anime in results:
                        f.write(f"🎭 {anime.get('title', '未知标题')}\n")
                        f.write(f"📺 集数: {anime.get('episodes', '未知')}\n")
                        f.write(f"🏷️  类型: {anime.get('genres_str', '未知')}\n")
                        f.write(f"🔗 详情页: {anime.get('detail_url', '')}\n")
                        f.write(f"🖼️  图片: {anime.get('image_url', '')}\n")
                        f.write(f"📝 简介: {anime.get('description', '暂无简介')}\n")
                        f.write("-" * 80 + "\n\n")
                        
            elif format_type == 'csv':
                import csv
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['标题', '集数', '类型', '详情链接', '图片链接', '动漫ID', '简介'])
                    
                    for anime in results:
                        writer.writerow([
                            anime.get('title', ''),
                            anime.get('episodes', ''),
                            anime.get('genres_str', ''),
                            anime.get('detail_url', ''),
                            anime.get('image_url', ''),
                            anime.get('anime_id', ''),
                            anime.get('description', '')
                        ])
            
            print(f"✅ 结果已导出到: {filename}")
            
        except Exception as e:
            print(f"❌ 导出失败: {str(e)}")

    def batch_search(self, keywords, output_dir=".", format_type='json'):
        """批量搜索"""
        all_results = {}
        
        for keyword in keywords:
            print(f"\n{'='*80}")
            print(f"正在搜索: {keyword}")
            print(f"{'='*80}")
            
            results = self.search_anime(keyword)
            all_results[keyword] = results
            
            # 为每个关键词单独保存
            if results:
                filename = f"search_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
                filepath = os.path.join(output_dir, filename)
                self.export_results(results, filepath, format_type)
        
        # 保存汇总结果
        summary_filename = f"batch_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        summary_path = os.path.join(output_dir, summary_filename)
        
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            print(f"\n📊 汇总结果已保存到: {summary_path}")
        except Exception as e:
            print(f"❌ 保存汇总结果失败: {str(e)}")

    def interactive_mode(self):
        """交互模式"""
        print("🌸 樱花动漫搜索工具 - 交互模式")
        print("输入关键词进行搜索，输入 'exit' 退出")
        print("-" * 50)
        
        while True:
            keyword = input("\n请输入搜索关键词: ").strip()
            if keyword.lower() == 'exit':
                print("👋 感谢使用！")
                break
            
            if not keyword:
                print("⚠️ 请输入有效的关键词")
                continue
            
            results = self.search_anime(keyword)
            
            if results:
                save = input("是否保存结果？(y/n): ").strip().lower()
                if save == 'y':
                    filename = f"search_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    self.export_results(results, filename, 'json')


def main():
    parser = argparse.ArgumentParser(description='樱花动漫搜索爬虫')
    parser.add_argument('keyword', nargs='?', help='搜索关键词')
    parser.add_argument('-f', '--file', help='从文件读取关键词列表')
    parser.add_argument('-o', '--output', default='.', help='输出目录')
    parser.add_argument('-t', '--format', choices=['json', 'txt', 'csv'], default='json', help='输出格式')
    parser.add_argument('-i', '--interactive', action='store_true', help='交互模式')
    
    args = parser.parse_args()
    
    crawler = AnimeSearchCLI()
    
    if args.interactive:
        crawler.interactive_mode()
    elif args.file:
        # 从文件读取关键词
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                keywords = [line.strip() for line in f if line.strip()]
            crawler.batch_search(keywords, args.output, args.format)
        except FileNotFoundError:
            print(f"❌ 文件未找到: {args.file}")
            sys.exit(1)
    elif args.keyword:
        # 单个关键词搜索
        results = crawler.search_anime(args.keyword)
        if results:
            filename = f"search_{args.keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"
            crawler.export_results(results, filename, args.format)
    else:
        # 交互模式
        crawler.interactive_mode()

if __name__ == "__main__":
    main()