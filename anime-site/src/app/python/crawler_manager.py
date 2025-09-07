#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫爬虫统一管理器
整合所有优化后的爬虫功能，提供统一的API接口
"""

import json
import sys
from typing import Dict, Any

# 导入所有优化后的爬虫
from crawler_search import search_anime
from crawler_all_anime import get_all_anime
from crawler_episodes import get_anime_episodes
from crawler_latest import get_latest_updates
from crawler_video import get_video_url

class CrawlerManager:
    """爬虫统一管理器"""
    
    def __init__(self):
        self.crawlers = {
            'search': search_anime,
            'all_anime': get_all_anime,
            'episodes': get_anime_episodes,
            'latest': get_latest_updates,
            'video': get_video_url
        }
    
    def run_crawler(self, crawler_type: str, **kwargs) -> Dict[str, Any]:
        """运行指定类型的爬虫
        
        Args:
            crawler_type: 爬虫类型 ('search', 'all_anime', 'episodes', 'latest', 'video')
            **kwargs: 爬虫特定参数
            
        Returns:
            统一格式的响应字典
        """
        if crawler_type not in self.crawlers:
            return {
                'success': False,
                'error': f'不支持的爬虫类型: {crawler_type}',
                'available_types': list(self.crawlers.keys()),
                'data': None
            }
        
        try:
            crawler_func = self.crawlers[crawler_type]
            
            # 根据爬虫类型处理参数
            if crawler_type == 'search':
                result = crawler_func(kwargs.get('keyword', ''))
            elif crawler_type == 'all_anime':
                result = crawler_func()
            elif crawler_type == 'episodes':
                result = crawler_func(kwargs.get('url', ''))
            elif crawler_type == 'latest':
                result = crawler_func(kwargs.get('limit', 50))
            elif crawler_type == 'video':
                result = crawler_func(kwargs.get('url', ''))
            else:
                result = {'success': False, 'error': '未知错误'}
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': None
            }
    
    def get_available_crawlers(self) -> Dict[str, str]:
        """获取可用的爬虫类型"""
        return {
            'search': '搜索动漫',
            'all_anime': '获取完整动漫列表',
            'episodes': '获取动漫分集信息',
            'latest': '获取最新更新',
            'video': '解析视频URL'
        }

def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("用法: python crawler_manager.py <crawler_type> [参数...]")
        print("可用爬虫类型:")
        manager = CrawlerManager()
        for crawler_type, description in manager.get_available_crawlers().items():
            print(f"  {crawler_type}: {description}")
        return
    
    crawler_type = sys.argv[1]
    manager = CrawlerManager()
    
    # 处理参数
    kwargs = {}
    if crawler_type == 'search' and len(sys.argv) > 2:
        kwargs['keyword'] = ' '.join(sys.argv[2:])
    elif crawler_type == 'episodes' and len(sys.argv) > 2:
        kwargs['url'] = sys.argv[2]
    elif crawler_type == 'latest' and len(sys.argv) > 2:
        try:
            kwargs['limit'] = int(sys.argv[2])
        except ValueError:
            kwargs['limit'] = 50
    elif crawler_type == 'video' and len(sys.argv) > 2:
        kwargs['url'] = sys.argv[2]
    
    # 运行爬虫
    result = manager.run_crawler(crawler_type, **kwargs)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()