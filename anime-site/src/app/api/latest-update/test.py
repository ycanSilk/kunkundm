#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Python爬虫调用的简单脚本
"""

import subprocess
import json
import os

def test_python_crawler():
    """测试Python爬虫调用"""
    try:
        # 获取当前工作目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        python_dir = os.path.join(current_dir, '..', 'python')
        
        # 构建Python命令
        python_path = os.path.join(python_dir, 'crawler_manager.py')
        cmd = ['python', python_path, 'latest', '5']
        
        print(f"执行命令: {' '.join(cmd)}")
        print(f"工作目录: {python_dir}")
        
        # 执行Python爬虫
        result = subprocess.run(
            cmd,
            cwd=python_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("返回码:", result.returncode)
        print("标准输出:", result.stdout)
        print("标准错误:", result.stderr)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print("成功获取数据:", len(data.get('data', [])))
            return data
        else:
            print("爬虫执行失败")
            return None
            
    except Exception as e:
        print("执行失败:", str(e))
        return None

if __name__ == "__main__":
    test_python_crawler()