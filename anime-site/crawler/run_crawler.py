#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫启动脚本
"""

import argparse
import sys
import os
from anime_crawler import MockAnimeCrawler

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description='动漫网站爬虫启动脚本')
    parser.add_argument('--type', choices=['mock', 'real'], default='mock',
                      help='爬虫类型：mock(模拟) 或 real(真实)')
    parser.add_argument('--api-url', default='http://localhost:3000',
                      help='后端API地址')
    parser.add_argument('--count', type=int, default=20,
                      help='模拟数据数量')
    parser.add_argument('--action', choices=['test', 'crawl'], default='test',
                      help='执行动作：test(测试连接) 或 crawl(爬取数据)')
    
    args = parser.parse_args()
    
    print("🚀 启动动漫爬虫...")
    print(f"📡 API地址: {args.api_url}")
    print(f"🔧 爬虫类型: {args.type}")
    print(f"📊 数据数量: {args.count}")
    
    try:
        crawler = MockAnimeCrawler(args.api_url)
        
        if args.action == 'test':
            print("\n🔍 测试后端连接...")
            status = crawler.get_status()
            if status.get('success'):
                print("✅ 后端API连接正常")
                print("📋 支持的爬虫类型:", status.get('supported_types', []))
            else:
                print("❌ 后端API连接失败")
                return 1
                
        elif args.action == 'crawl':
            print("\n📦 开始爬取数据...")
            
            # 发送动漫列表
            anime_list = crawler.generate_mock_anime_list(args.count)
            result = crawler.send_data("anime_list", anime_list)
            
            if result.get('success'):
                print("✅ 数据爬取完成")
            else:
                print("❌ 数据爬取失败")
                return 1
    
    except KeyboardInterrupt:
        print("\n⏹️  用户中断")
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)