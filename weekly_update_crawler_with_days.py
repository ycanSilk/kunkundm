#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫首页每周更新列表爬虫 - 按周一到周日分类
爬取 http://www.iyinghua.com/ 首页的每周更新列表
按周一到周日7个ul数组进行分类，第一个是周一，最后一个是周日
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin
from datetime import datetime

def crawl_weekly_updates_with_days():
    """爬取首页每周更新列表并按周一到周日分类"""
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
            return {}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找每周更新列表，按周一到周日分类
        weekly_updates = {
            "周一": [],
            "周二": [],
            "周三": [],
            "周四": [],
            "周五": [],
            "周六": [],
            "周日": []
        }
        
        # 使用指定的选择器查找更新列表
        tlist_elements = soup.select('.area .side .bg .tlist ul')
        
        print(f"找到 {len(tlist_elements)} 个更新列表区域")
        
        # 将7个ul对应到周一到周日
        days_mapping = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        
        for list_idx, tlist in enumerate(tlist_elements):
            if list_idx >= 7:  # 只处理前7个ul
                break
                
            current_day = days_mapping[list_idx]
            
            # 获取该列表中的所有li元素
            li_elements = tlist.find_all('li')
            
            print(f"{current_day}: 找到 {len(li_elements)} 个更新条目")
            
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
                    
                    # 提取更新信息
                    spans = li.find_all('span')
                    update_info = []
                    for span in spans:
                        text = span.get_text(strip=True)
                        if text and text != update_data['title']:
                            update_info.append(text)
                    
                    update_data['update_info'] = ' '.join(update_info)
                    update_data['full_text'] = full_text
                    update_data['raw_html'] = str(li)
                    update_data['day'] = current_day
                    update_data['item_index'] = li_idx
                    
                    weekly_updates[current_day].append(update_data)
                    
                    # 打印前几个作为示例
                    if li_idx <= 3:
                        print(f"  [{li_idx}] {update_data['title']} - {update_data['full_text']}")
                        print(f"      链接: {update_data['url']}")
                        print("  " + "-" * 30)
                    
                except Exception as e:
                    print(f"处理第{li_idx}个条目时出错: {e}")
                    continue
        
        return weekly_updates
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return {}
    except Exception as e:
        print(f"发生错误: {e}")
        return {}

def save_to_json(data, filename="weekly_updates_by_days.json"):
    """保存数据到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        total_items = sum(len(items) for items in data.values())
        print(f"数据已保存到: {filename}")
        print(f"共保存了 {total_items} 个更新条目")
        
        for day, items in data.items():
            print(f"{day}: {len(items)} 个更新")
            
    except Exception as e:
        print(f"保存文件时出错: {e}")

def create_html_viewer_with_days(data, filename="每周更新列表_按日期分类.html"):
    """创建按周一到周日分类的HTML查看器"""
    html_content = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>樱花动漫 - 每周更新列表（按日期分类）</title>
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
            max-width: 1200px;
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
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .stat-item {
            text-align: center;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 15px;
        }

        .stat-number {
            font-size: 1.5em;
            font-weight: bold;
            display: block;
        }

        .days-container {
            padding: 20px;
        }

        .day-section {
            margin-bottom: 30px;
        }

        .day-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .day-title {
            font-size: 1.5em;
            font-weight: bold;
        }

        .day-count {
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
        }

        .update-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }

        .update-item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 15px;
            transition: all 0.3s;
        }

        .update-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-color: #667eea;
        }

        .update-title {
            font-size: 1.1em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }

        .update-info {
            color: #666;
            margin-bottom: 10px;
            font-size: 13px;
            line-height: 1.4;
        }

        .update-link {
            display: inline-block;
            padding: 6px 12px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 15px;
            font-size: 12px;
            transition: all 0.3s;
        }

        .update-link:hover {
            background: #5a6fd8;
            transform: scale(1.05);
        }

        .empty-day {
            text-align: center;
            padding: 30px;
            color: #999;
            font-style: italic;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .update-list {
                grid-template-columns: 1fr;
            }
            
            .stats {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📅 樱花动漫每周更新列表</h1>
            <p>按周一到周日分类的最新动漫更新</p>
            <div class="stats">
    '''

    total_items = sum(len(items) for items in data.values())
    
    for day, items in data.items():
        html_content += f'''
                <div class="stat-item">
                    <span class="stat-number">{len(items)}</span>
                    <span>{day}</span>
                </div>
        '''
    
    html_content += '''
            </div>
        </div>

        <div class="days-container">
    '''

    for day, updates in data.items():
        html_content += f'''
            <div class="day-section">
                <div class="day-header">
                    <div class="day-title">{day}</div>
                    <div class="day-count">{len(updates)} 个更新</div>
                </div>
                <div class="update-list">
        '''
        
        if updates:
            for update in updates:
                html_content += f'''
                    <div class="update-item">
                        <div class="update-title">{update['title']}</div>
                        <div class="update-info">{update['full_text']}</div>
                        <a href="{update['url']}" target="_blank" class="update-link">立即观看</a>
                    </div>
                '''
        else:
            html_content += '<div class="empty-day">今日暂无更新</div>'
        
        html_content += '''
                </div>
            </div>
        '''

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
    print("樱花动漫每周更新列表爬虫 - 按周一到周日分类")
    print("=" * 80)
    
    weekly_data = crawl_weekly_updates_with_days()
    
    if weekly_data:
        # 保存到JSON文件
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        json_filename = f"weekly_updates_by_days_{timestamp}.json"
        save_to_json(weekly_data, json_filename)
        
        # 创建HTML查看器
        html_filename = f"每周更新列表_按日期分类_{timestamp}.html"
        create_html_viewer_with_days(weekly_data, html_filename)
        
        # 显示详细统计
        total_items = sum(len(items) for items in weekly_data.values())
        print("\n" + "=" * 60)
        print("爬取完成！")
        print(f"总计: {total_items} 个更新条目")
        
        # 显示每个星期的更新情况
        for day, updates in weekly_data.items():
            if updates:
                print(f"\n{day} ({len(updates)} 个更新):")
                for i, update in enumerate(updates[:5], 1):
                    print(f"  {i}. {update['full_text']}")
                if len(updates) > 5:
                    print(f"  ... 还有 {len(updates) - 5} 个")
            else:
                print(f"\n{day}: 暂无更新")
        
    else:
        print("未能获取到更新数据")

if __name__ == "__main__":
    main()