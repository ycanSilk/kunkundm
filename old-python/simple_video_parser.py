#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫视频URL解析器 - 简化版
纯Python实现，使用requests和正则表达式解析
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import re
import json
from urllib.parse import urlparse
import threading
import time
from datetime import datetime

class SimpleVideoParser:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌸 樱花动漫视频URL解析器 - 简化版")
        self.root.geometry("800x600")
        self.root.configure(bg='#f8f9fa')
        
        # 设置样式
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """设置UI样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 按钮样式
        style.configure('Primary.TButton', 
                       background='#007bff', 
                       foreground='white',
                       borderwidth=1,
                       focusthickness=3,
                       focuscolor='none')
        style.map('Primary.TButton',
                 background=[('active', '#0056b3')])
                 
    def setup_ui(self):
        """设置UI界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = tk.Label(
            main_frame, 
            text="🌸 樱花动漫视频URL解析器", 
            font=("Microsoft YaHei", 18, "bold"),
            fg="#2c3e50",
            bg="#f8f9fa"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL输入区域
        url_frame = ttk.LabelFrame(main_frame, text="🔗 URL输入", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, font=("Consolas", 11), width=60)
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.url_entry.insert(0, "http://www.iyinghua.com/v/6543-1.html")
        
        # 按钮区域
        button_frame = ttk.Frame(url_frame)
        button_frame.grid(row=0, column=1)
        
        self.parse_btn = ttk.Button(
            button_frame,
            text="🔍 解析",
            command=self.start_parsing,
            style='Primary.TButton'
        )
        self.parse_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="🗑️ 清空",
            command=self.clear_all
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.copy_btn = ttk.Button(
            button_frame,
            text="📋 复制",
            command=self.copy_result,
            state="disabled"
        )
        self.copy_btn.pack(side=tk.LEFT)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="📊 解析结果", padding="10")
        result_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            font=("Consolas", 10),
            height=12,
            wrap=tk.WORD,
            bg="#ffffff",
            fg="#2c3e50"
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="📝 解析日志", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            height=8,
            wrap=tk.WORD,
            bg="#2b2b2b",
            fg="#ffffff"
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 进度条
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        # 配置权重
        main_frame.rowconfigure(2, weight=3)
        main_frame.rowconfigure(3, weight=2)
        
    def log_message(self, message, level="INFO"):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "INFO": "#00ff00",
            "WARNING": "#ffff00", 
            "ERROR": "#ff0000",
            "SUCCESS": "#00ff00",
            "DEBUG": "#888888"
        }
        
        self.log_text.insert(tk.END, f"[{timestamp}] [{level}] {message}\n")
        self.log_text.tag_add(level, f"{self.log_text.index(tk.END)}-2l", f"{self.log_text.index(tk.END)}-1l")
        self.log_text.tag_config(level, foreground=color_map.get(level, "#ffffff"))
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def extract_video_url_simple(self, html_content, page_url):
        """简化的视频URL提取"""
        self.log_message("🔍 开始提取视频URL...", "DEBUG")
        
        try:
            # 提取页面标题
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "未知视频"
            self.log_message(f"📄 页面标题: {title}")
            
            # 提取集数信息
            episode_match = re.search(r'第(\d+)集', title)
            current_episode = int(episode_match.group(1)) if episode_match else 1
            
            # 多种提取策略
            video_url = None
            
            # 策略1: 查找tup格式URL
            patterns = [
                r'["\'](https?://tup\.iyinghua\.com/[^"\']*\.m3u8[^"\']*)["\']',
                r'["\'](https?://[^"\']*bf8bf\.com[^"\']*\.m3u8[^"\']*)["\']',
                r'["\']vid["\']:\s*["\'](https?://[^"\']+\.m3u8[^"\']*)["\']',
                r'(https?://[^"\']+\.m3u8[^"\']*)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    video_url = matches[0]
                    if not video_url.startswith('http'):
                        video_url = f"https://tup.iyinghua.com/?vid={video_url}"
                    self.log_message(f"✅ 找到视频URL: {video_url}")
                    break
            
            # 计算总集数
            total_episodes = 12
            total_match = re.search(r'共(\d+)集', html_content)
            if total_match:
                total_episodes = int(total_match.group(1))
                
            return {
                'video_url': video_url,
                'title': title,
                'current_episode': current_episode,
                'total_episodes': total_episodes,
                'source_url': page_url
            }
            
        except Exception as e:
            self.log_message(f"❌ 提取失败: {str(e)}", "ERROR")
            return {
                'video_url': None,
                'title': '解析失败',
                'current_episode': 1,
                'total_episodes': 1,
                'source_url': page_url,
                'error': str(e)
            }
            
    def parse_video_url_simple(self, url):
        """简化的视频解析"""
        self.log_message(f"🚀 开始解析: {url}")
        
        try:
            # 验证URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                self.log_message("❌ 无效的URL格式", "ERROR")
                return None
                
            # 设置请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            self.log_message("🌐 发送HTTP请求...")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            self.log_message(f"✅ 获取页面成功 ({len(response.text)} 字符)")
            
            # 提取视频信息
            result = self.extract_video_url_simple(response.text, url)
            return result
            
        except requests.RequestException as e:
            self.log_message(f"❌ 网络请求失败: {str(e)}", "ERROR")
            return None
        except Exception as e:
            self.log_message(f"❌ 解析失败: {str(e)}", "ERROR")
            return None
            
    def start_parsing(self):
        """开始解析"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入有效的URL")
            return
            
        # 禁用按钮
        self.parse_btn.config(state="disabled")
        self.copy_btn.config(state="disabled")
        self.progress.start()
        
        # 清空内容
        self.result_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        
        # 后台线程解析
        thread = threading.Thread(target=self.parse_in_background, args=(url,))
        thread.daemon = True
        thread.start()
        
    def parse_in_background(self, url):
        """后台解析"""
        try:
            result = self.parse_video_url_simple(url)
            
            if result:
                # 格式化显示结果
                formatted_result = f"""
🌸 樱花动漫视频解析结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 视频信息:
   标题: {result['title']}
   当前集数: 第 {result['current_episode']} 集
   总集数: {result['total_episodes']} 集
   原始URL: {result['source_url']}

🎬 真实视频URL:
{result['video_url'] or '❌ 未找到真实视频URL'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 使用说明:
   如果未找到真实URL，可能是:
   1. 页面结构发生变化
   2. 需要更复杂的解析方法
   3. 视频已下架或链接失效
                """
                
                self.result_text.insert(tk.END, formatted_result)
                self.copy_btn.config(state="normal")
                
                if result['video_url']:
                    self.log_message("✅ 解析成功！真实视频URL已提取", "SUCCESS")
                else:
                    self.log_message("⚠️ 解析完成，但未找到真实视频URL", "WARNING")
            else:
                self.result_text.insert(tk.END, "❌ 解析失败，请查看日志获取详细信息")
                self.log_message("❌ 解析失败", "ERROR")
                
        except Exception as e:
            error_msg = f"解析过程中发生错误: {str(e)}"
            self.result_text.insert(tk.END, error_msg)
            self.log_message(error_msg, "ERROR")
            
        finally:
            # 恢复按钮状态
            self.parse_btn.config(state="normal")
            self.progress.stop()
            
    def clear_all(self):
        """清空所有内容"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "http://www.iyinghua.com/v/6543-1.html")
        self.result_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.copy_btn.config(state="disabled")
        
    def copy_result(self):
        """复制结果到剪贴板"""
        result = self.result_text.get(1.0, tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "解析结果已复制到剪贴板")
            
    def run(self):
        """运行应用"""
        self.log_message("🌸 樱花动漫视频解析器已启动")
        self.log_message("💡 请输入樱花动漫页面URL进行解析")
        self.root.mainloop()

if __name__ == "__main__":
    # 检查必要的库
    required_packages = ['requests', 'beautifulsoup4']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'beautifulsoup4':
                import bs4
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 请安装以下依赖包:")
        print(f"pip install {' '.join(missing_packages)}")
        import sys
        sys.exit(1)
        
    app = SimpleVideoParser()
    app.run()