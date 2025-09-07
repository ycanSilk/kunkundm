#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import sys

def get_real_video_url(page_url: str) -> str:
    """爬取真实视频URL并返回"""
    try:
        html = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3).text
        soup = BeautifulSoup(html, 'lxml')
        
        # 查找data-vid属性
        vid = (soup.find('div', id='playbox') or {}).get('data-vid')
        if not vid:
            for div in soup.find_all('div', {'data-vid': True}):
                if div.get('data-vid', '').startswith('http'):
                    vid = div['data-vid']
                    break
        
        if vid:
            # 只提取干净的URL片段，不做任何拼接
            # 去除/index.m3u8$mp4后缀，返回基础路径
            base_path = vid.replace('/index.m3u8$mp4', '')
            
            # 找到最后一个斜杠的位置，获取目录名
            last_slash_index = base_path.rfind('/')
            if last_slash_index != -1:
                # 返回基础URL和目录名，让后端处理拼接
                clean_base_url = base_path[:last_slash_index]  # 不包含最后一级目录
                return clean_base_url
            
            # 如果没有斜杠，返回原始URL
            return vid
        return ""
    except:
        return ""

if __name__ == "__main__":
    import os
    import sys
    
    # 设置环境变量以支持UTF-8编码
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # 确保标准输出使用UTF-8编码
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    
    try:
        url = get_real_video_url(sys.argv[1] if len(sys.argv) > 1 else "http://www.iyinghua.com/v/6473-1.html")
        result = json.dumps({'url': url}, ensure_ascii=False)
        print(result)
    except UnicodeEncodeError as e:
        # 如果仍然出现编码错误，使用ASCII转义
        url = get_real_video_url(sys.argv[1] if len(sys.argv) > 1 else "http://www.iyinghua.com/v/6473-1.html")
        result = json.dumps({'url': url}, ensure_ascii=True)
        print(result)
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False))