#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫首页每周更新列表爬虫
爬取 http://www.iyinghua.com/ 首页的每周更新列表
选择器：.area .side .bg .tlist ul 和 .area .side .bg .tlist ul li
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

def crawl_weekly_updates():
    """爬取首页每周更新列表"""
    base_url = "http://www.iyinghua.com"
    url = base_url
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print("正在访问樱花动漫首页...")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"访问失败，状态码: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找每周更新列表
        weekly_updates = []
        
        # 使用指定的选择器查找更新列表
        tlist_elements = soup.select('.area .side .bg .tlist ul')
        
        print(f"找到 {len(tlist_elements)} 个更新列表区域")
        
        for list_idx, tlist in enumerate(tlist_elements, 1):
            # 获取该列表中的所有li元素
            li_elements = tlist.find_all('li')
            
            print(f"列表 {list_idx}: 找到 {len(li_elements)} 个更新条目")
            
            for li_idx, li in enumerate(li_elements, 1):
                try:
                    update_data = {}
                    
                    # 提取完整文本
                    full_text = li.get_text(strip=True)
                    
                    # 提取动漫信息
                    title_link = li.find('a')
                    if title_link:
                        update_data['title'] = title_link.get_text(strip=True)
                        update_data['url'] = urljoin(base_url, title_link.get('href', ''))
                    else:
                        update_data['title'] = full_text
                        update_data['url'] = ''
                    
                    # 提取更新信息（如果有span或其他标签）
                    spans = li.find_all('span')
                    update_info = []
                    for span in spans:
                        text = span.get_text(strip=True)
                        if text and text != update_data['title']:
                            update_info.append(text)
                    
                    update_data['update_info'] = ' '.join(update_info)
                    update_data['full_text'] = full_text
                    update_data['raw_html'] = str(li)
                    update_data['list_index'] = list_idx
                    update_data['item_index'] = li_idx
                    
                    weekly_updates.append(update_data)
                    
                    # 打印前几个作为示例
                    if li_idx <= 3:
                        print(f"  [{li_idx}] {update_data['title']} - {update_data['update_info']}")
                        print(f"      链接: {update_data['url']}")
                        print(f"      完整文本: {full_text}")
                        print("  " + "-" * 40)
                    
                except Exception as e:
                    print(f"处理第{li_idx}个条目时出错: {e}")
                    continue
        
        return weekly_updates
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return []
    except Exception as e:
        print(f"发生错误: {e}")
        return []

def save_to_json(data, filename="weekly_updates.json"):
    """保存数据到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filename}")
        print(f"共保存了 {len(data)} 个更新条目")
    except Exception as e:
        print(f"保存文件时出错: {e}")

def create_html_viewer(data, filename="每周更新列表.html"):
    """创建HTML查看器"""
    html_content = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>樱花动漫 - 每周更新列表</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #ff6b6b, #ffa726);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 15px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }

        .update-list {
            padding: 30px;
        }

        .update-item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }

        .update-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-color: #667eea;
        }

        .update-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }

        .update-info {
            color: #666;
            margin-bottom: 10px;
            font-size: 14px;
        }

        .update-link {
            display: inline-block;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 20px;
            font-size: 14px;
            transition: all 0.3s;
        }

        .update-link:hover {
            background: #5a6fd8;
            transform: scale(1.05);
        }

        .no-data {
            text-align: center;
            padding: 50px;
            color: #666;
            font-size: 1.2em;
        }

        .loading {
            text-align: center;
            padding: 50px;
            font-size: 1.2em;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📅 樱花动漫每周更新列表</h1>
            <p>最新动漫更新一览</p>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">''' + str(len(data)) + '''</span>
                    <span>更新条目</span>
                </div>
            </div>
        </div>

        <div class="update-list">
    '''

    if data:
        for item in data:
            html_content += f'''
                <div class="update-item">
                    <div class="update-title">{item['title']}</div>
                    <div class="update-info">{item['full_text']}</div>
                    <a href="{item['url']}" target="_blank" class="update-link">立即观看</a>
                </div>
            '''
    else:
        html_content += '<div class="no-data">暂无更新数据</div>'

    html_content += '''
        </div>
    </div>
</body>
</html>
    '''

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML查看器已创建: {filename}")
    except Exception as e:
        print(f"创建HTML查看器时出错: {e}")

def main():
    """主函数"""
    print("=" * 80)
    print("樱花动漫每周更新列表爬虫")
    print("=" * 80)
    
    weekly_data = crawl_weekly_updates()
    
    if weekly_data:
        # 保存到JSON文件
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        json_filename = f"weekly_updates_{timestamp}.json"
        save_to_json(weekly_data, json_filename)
        
        # 创建HTML查看器
        html_filename = f"每周更新列表_{timestamp}.html"
        create_html_viewer(weekly_data, html_filename)
        
        # 显示统计信息
        print("\n" + "=" * 60)
        print("爬取完成！")
        print(f"总计: {len(weekly_data)} 个更新条目")
        
        # 显示前10个作为预览
        print("\n前10个更新预览:")
        for i, update in enumerate(weekly_data[:10], 1):
            print(f"{i:2d}. {update['title']} - {update['full_text']}")
        
    else:
        print("未能获取到更新数据")

if __name__ == "__main__":
    main()