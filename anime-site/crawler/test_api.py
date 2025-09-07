#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本
"""

import requests
import json

def test_api():
    """测试API功能"""
    api_url = "http://localhost:3000/api/crawler"
    
    # 测试数据
    test_data = {
        "crawler_type": "anime_list",
        "data": [
            {
                "id": "1",
                "title": "测试动漫",
                "coverImage": "https://via.placeholder.com/300x400",
                "episodes": 12,
                "currentEpisode": 8,
                "genre": ["奇幻", "冒险"]
            }
        ],
        "source_url": "https://example.com"
    }
    
    try:
        print("🔍 测试API连接...")
        
        # 发送测试数据
        response = requests.post(api_url, json=test_data, timeout=10)
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📦 响应内容: {response.text}")
        
        # 测试获取数据
        list_response = requests.get("http://localhost:3000/api/anime?action=list")
        print(f"📋 动漫列表: {list_response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    test_api()