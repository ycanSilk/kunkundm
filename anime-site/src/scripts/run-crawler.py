#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动漫站点爬虫集成服务
用于从Next.js应用调用Python爬虫脚本
"""

import sys
import os
import json
import subprocess
from pathlib import Path

# 添加爬虫脚本路径
sys.path.append(str(Path(__file__).parent.parent.parent))

def run_latest_update_crawler():
    """运行最新更新爬虫"""
    try:
        # 构建爬虫脚本路径
        crawler_path = Path(__file__).parent.parent.parent / "最新更新" / "latest_update_crawler.py"
        
        if not crawler_path.exists():
            return {
                "success": False,
                "error": f"爬虫脚本不存在: {crawler_path}"
            }
        
        # 运行爬虫
        result = subprocess.run([
            sys.executable,
            str(crawler_path)
        ], capture_output=True, text=True, cwd=str(crawler_path.parent))
        
        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr
            }
        
        # 查找生成的JSON文件
        json_files = list(crawler_path.parent.glob("latest_updates_*.json"))
        if not json_files:
            return {
                "success": False,
                "error": "未找到生成的JSON文件"
            }
        
        # 读取最新生成的文件
        latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    """主函数 - 处理命令行参数"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "请指定爬虫类型: latest_update, search, complete_list, episodes, video_parser"
        }))
        return
    
    crawler_type = sys.argv[1]
    
    if crawler_type == "latest_update":
        result = run_latest_update_crawler()
    elif crawler_type == "search":
        # TODO: 集成搜索爬虫
        result = {"success": False, "error": "搜索爬虫未实现"}
    elif crawler_type == "complete_list":
        # TODO: 集成完整列表爬虫
        result = {"success": False, "error": "完整列表爬虫未实现"}
    elif crawler_type == "episodes":
        # TODO: 集成集数爬虫
        result = {"success": False, "error": "集数爬虫未实现"}
    elif crawler_type == "video_parser":
        # TODO: 集成视频解析爬虫
        result = {"success": False, "error": "视频解析爬虫未实现"}
    else:
        result = {"success": False, "error": f"未知的爬虫类型: {crawler_type}"}
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()