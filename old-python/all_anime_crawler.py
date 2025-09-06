#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫全部动漫列表爬虫
爬取 http://www.iyinghua.com/all/ 页面的所有动漫数据
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

def crawl_all_anime():
    """爬取全部动漫列表"""
    base_url = "http://www.iyinghua.com"
    url = f"{base_url}/all/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print("正在访问樱花动漫全部动漫页面...")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"访问失败，状态码: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据提供的CSS选择器定位动漫列表
        anime_list = []
        
        # 查找所有符合条件的li元素
        li_elements = soup.select('body > div:nth-child(5) > div:nth-child(1) > ul > li')
        
        print(f"找到 {len(li_elements)} 个动漫条目")
        
        for idx, li in enumerate(li_elements, 1):
            try:
                anime_data = {}
                
                # 提取序号
                if li.text.strip():
                    text_content = li.get_text(strip=True)
                    # 提取序号（数字前缀）
                    import re
                    match = re.match(r'(\d+)\.(.+)', text_content)
                    if match:
                        anime_data['index'] = int(match.group(1))
                        anime_data['full_text'] = match.group(2)
                    else:
                        anime_data['index'] = idx
                        anime_data['full_text'] = text_content
                
                # 提取动漫名称和链接
                title_link = li.find('a', target="_blank")
                if title_link:
                    anime_data['title'] = title_link.get_text(strip=True)
                    anime_data['detail_url'] = urljoin(base_url, title_link.get('href', ''))
                else:
                    anime_data['title'] = li.get_text(strip=True)
                    anime_data['detail_url'] = ""
                
                # 提取集数信息
                episode_link = li.find('em').find('a') if li.find('em') else None
                if episode_link:
                    anime_data['episode_info'] = episode_link.get_text(strip=True)
                    anime_data['episode_url'] = urljoin(base_url, episode_link.get('href', ''))
                else:
                    anime_data['episode_info'] = ""
                    anime_data['episode_url'] = ""
                
                # 提取原始HTML
                anime_data['raw_html'] = str(li)
                
                anime_list.append(anime_data)
                
                # 打印前几个作为示例
                if idx <= 5:
                    print(f"[{anime_data['index']}] {anime_data['title']} - {anime_data['episode_info']}")
                    print(f"   详情: {anime_data['detail_url']}")
                    print(f"   播放: {anime_data['episode_url']}")
                    print("-" * 50)
                
            except Exception as e:
                print(f"处理第{idx}个条目时出错: {e}")
                continue
        
        return anime_list
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return []
    except Exception as e:
        print(f"发生错误: {e}")
        return []

def save_to_json(data, filename="all_anime_list.json"):
    """保存数据到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filename}")
        print(f"共保存了 {len(data)} 个动漫条目")
    except Exception as e:
        print(f"保存文件时出错: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("樱花动漫全部动漫列表爬虫")
    print("=" * 60)
    
    anime_data = crawl_all_anime()
    
    if anime_data:
        # 保存到JSON文件
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"all_anime_list_{timestamp}.json"
        save_to_json(anime_data, filename)
        
        # 显示统计信息
        print("\n" + "=" * 60)
        print("爬取完成！")
        print(f"总计: {len(anime_data)} 个动漫")
        
        # 显示前10个作为预览
        print("\n前10个动漫预览:")
        for i, anime in enumerate(anime_data[:10], 1):
            print(f"{i:2d}. {anime['title']} - {anime['episode_info']}")
        
    else:
        print("未能获取到动漫数据")

if __name__ == "__main__":
    main()