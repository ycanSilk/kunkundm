#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫完整动漫列表爬虫
爬取 http://m.iyinghua.com/all/ 页面的所有分类动漫数据
包含A-Z和全部分类，共27个分类
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

def crawl_complete_all_anime():
    """爬取完整的所有分类动漫列表"""
    base_url = "http://m.iyinghua.com"
    url = f"{base_url}/all/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print("正在访问樱花动漫完整动漫页面...")
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"访问失败，状态码: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有分类的动漫列表
        all_anime_data = []
        category_count = 0
        
        # 查找所有<div class="mlist">标签
        mlist_divs = soup.find_all('div', class_='mlist')
        
        print(f"找到 {len(mlist_divs)} 个分类")
        
        for category_idx, mlist_div in enumerate(mlist_divs, 1):
            # 获取分类信息
            category_name = "未知分类"
            
            # 查找分类标题（通常在li class="man"中的a标签）
            category_link = mlist_div.find('li', class_='man')
            if category_link:
                category_name = category_link.find('a').get_text(strip=True) if category_link.find('a') else f"分类{category_idx}"
            
            print(f"正在处理分类: {category_name} ({category_idx}/{len(mlist_divs)})")
            
            # 获取该分类下的所有li标签
            li_elements = mlist_div.find_all('li')
            
            category_anime = []
            anime_count = 0
            
            for li_idx, li in enumerate(li_elements, 1):
                try:
                    anime_data = {}
                    
                    # 跳过分类标题行
                    if 'man' in li.get('class', []):
                        continue
                    
                    # 提取序号
                    full_text = li.get_text(strip=True)
                    
                    # 提取动漫信息
                    title_link = li.find('a', target="_blank")
                    if title_link:
                        anime_data['title'] = title_link.get_text(strip=True)
                        anime_data['detail_url'] = urljoin(base_url, title_link.get('href', ''))
                    else:
                        # 尝试其他方式获取标题
                        all_links = li.find_all('a')
                        if len(all_links) > 0:
                            anime_data['title'] = all_links[0].get_text(strip=True)
                            anime_data['detail_url'] = urljoin(base_url, all_links[0].get('href', ''))
                        else:
                            anime_data['title'] = full_text
                            anime_data['detail_url'] = ""
                    
                    # 提取集数信息
                    episode_info = ""
                    episode_url = ""
                    
                    # 查找em标签中的集数信息
                    em_tag = li.find('em')
                    if em_tag:
                        episode_link = em_tag.find('a')
                        if episode_link:
                            episode_info = episode_link.get_text(strip=True)
                            episode_url = urljoin(base_url, episode_link.get('href', ''))
                        else:
                            episode_info = em_tag.get_text(strip=True)
                    
                    anime_data['episode_info'] = episode_info
                    anime_data['episode_url'] = episode_url
                    anime_data['category'] = category_name
                    anime_data['full_text'] = full_text
                    anime_data['raw_html'] = str(li)
                    
                    category_anime.append(anime_data)
                    anime_count += 1
                    
                except Exception as e:
                    print(f"处理第{li_idx}个条目时出错: {e}")
                    continue
            
            # 添加到总列表
            all_anime_data.extend(category_anime)
            category_count += 1
            
            print(f"  分类 {category_name}: 获取了 {anime_count} 个动漫")
            
            # 避免请求过快
            time.sleep(0.1)
        
        return all_anime_data
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return []
    except Exception as e:
        print(f"发生错误: {e}")
        return []

def save_to_json(data, filename="complete_all_anime_list.json"):
    """保存数据到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filename}")
        print(f"共保存了 {len(data)} 个动漫条目")
    except Exception as e:
        print(f"保存文件时出错: {e}")

def analyze_data(data):
    """分析数据"""
    if not data:
        return
    
    # 按分类统计
    category_stats = {}
    for anime in data:
        category = anime.get('category', '未知')
        if category not in category_stats:
            category_stats[category] = 0
        category_stats[category] += 1
    
    print("\n" + "=" * 60)
    print("数据统计:")
    print("=" * 60)
    for category, count in sorted(category_stats.items()):
        print(f"{category}: {count} 个")
    
    # 显示前20个动漫
    print("\n前20个动漫预览:")
    for i, anime in enumerate(data[:20], 1):
        print(f"{i:3d}. [{anime.get('category', '未知')}] {anime['title']} - {anime['episode_info']}")

def main():
    """主函数"""
    print("=" * 80)
    print("樱花动漫完整动漫列表爬虫")
    print("爬取所有分类(A-Z+其他)的完整动漫数据")
    print("=" * 80)
    
    anime_data = crawl_complete_all_anime()
    
    if anime_data:
        # 保存到JSON文件
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"complete_all_anime_list_{timestamp}.json"
        save_to_json(anime_data, filename)
        
        # 分析数据
        analyze_data(anime_data)
        
    else:
        print("未能获取到动漫数据")

if __name__ == "__main__":
    main()