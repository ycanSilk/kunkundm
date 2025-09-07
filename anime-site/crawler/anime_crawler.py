#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动漫网站爬虫脚本
用于爬取动漫数据并发送到Next.js后端API
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnimeCrawler:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/crawler"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AnimeCrawler/1.0.0'
        })
    
    def send_data(self, crawler_type: str, data: Any, source_url: str = None) -> Dict:
        """发送数据到后端API"""
        payload = {
            "crawler_type": crawler_type,
            "data": data,
            "source_url": source_url,
            "timestamp": datetime.now().isoformat(),
            "crawler_version": "1.0.0",
            "batch_id": f"batch_{int(time.time())}"
        }
        
        try:
            response = self.session.post(self.api_endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                logger.info(f"✅ 成功发送 {crawler_type} 数据: {len(data) if isinstance(data, list) else len(data) if isinstance(data, dict) else 1} 条记录")
            else:
                logger.error(f"❌ 发送失败: {result.get('error')}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 网络请求失败: {e}")
            return {"success": False, "error": str(e)}
    
    def get_status(self) -> Dict:
        """获取后端API状态"""
        try:
            response = self.session.get(f"{self.api_endpoint}?action=status")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 获取状态失败: {e}")
            return {"success": False, "error": str(e)}

class MockAnimeCrawler(AnimeCrawler):
    """模拟爬虫，用于测试"""
    
    def generate_mock_anime_list(self, count: int = 10) -> List[Dict]:
        """生成模拟动漫列表数据"""
        mock_animes = []
        genres = ["奇幻", "冒险", "科幻", "动作", "喜剧", "悬疑", "校园", "恋爱"]
        
        for i in range(1, count + 1):
            anime = {
                "id": str(i),
                "title": f"测试动漫 {i}",
                "coverImage": f"https://via.placeholder.com/300x400/{i*123456%16777215:06x}/FFFFFF?text=动漫{i}",
                "episodes": 12 + (i % 13),
                "currentEpisode": min(12 + (i % 13), 8 + (i % 5)),
                "genre": [genres[i % len(genres)], genres[(i + 1) % len(genres)]],
                "description": f"这是测试动漫 {i} 的简介，包含了精彩的故事情节和人物设定。",
                "year": 2024 - (i % 3),
                "rating": 7.5 + (i % 25) / 10
            }
            mock_animes.append(anime)
        
        return mock_animes
    
    def generate_mock_weekly_updates(self) -> Dict[str, List[Dict]]:
        """生成模拟每周更新数据"""
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekly_data = {}
        
        for day in days:
            updates = []
            for i in range(1, 6):
                update = {
                    "id": f"{day}_{i}",
                    "title": f"{day}更新动漫{i}",
                    "episode": 8 + i,
                    "coverImage": f"https://via.placeholder.com/60x80/{hash(day+i)%16777215:06x}/FFFFFF?text={i}",
                    "genre": ["奇幻", "冒险"]
                }
                updates.append(update)
            weekly_data[day] = updates
        
        return weekly_data

def main():
    """主函数 - 用于测试爬虫"""
    crawler = MockAnimeCrawler()
    
    # 检查后端状态
    logger.info("检查后端API状态...")
    status = crawler.get_status()
    if status.get('success'):
        logger.info("✅ 后端API连接正常")
    else:
        logger.error("❌ 后端API连接失败")
        return
    
    # 发送模拟数据
    logger.info("开始发送模拟数据...")
    
    # 发送动漫列表
    anime_list = crawler.generate_mock_anime_list(20)
    result1 = crawler.send_data("anime_list", anime_list, "https://example.com/anime")
    
    # 发送每周更新
    weekly_updates = crawler.generate_mock_weekly_updates()
    result2 = crawler.send_data("weekly_updates", weekly_updates, "https://example.com/weekly")
    
    # 发送搜索结果
    search_results = crawler.generate_mock_anime_list(5)
    result3 = crawler.send_data("search_results", search_results, "https://example.com/search")
    
    logger.info("数据发送完成！")

if __name__ == "__main__":
    main()