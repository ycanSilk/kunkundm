#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫视频URL解析器 - 可视化版本
独立运行的Python脚本，专门解析樱花动漫页面URL为真实视频地址
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse
import threading
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

class VideoParserGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌸 樱花动漫视频URL解析器")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # 设置窗口图标
        try:
            self.root.iconbitmap(default='')
        except:
            pass
            
        self.setup_ui()
        self.driver = None
        
    def setup_ui(self):
        """设置UI界面"""
        # 标题
        title_label = tk.Label(
            self.root, 
            text="🌸 樱花动漫视频URL解析器", 
            font=("Arial", 20, "bold"),
            fg="#667eea",
            bg="#f0f0f0"
        )
        title_label.pack(pady=10)
        
        # 输入区域
        input_frame = tk.LabelFrame(
            self.root, 
            text="🔗 URL输入", 
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        )
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # URL输入框
        self.url_entry = tk.Entry(
            input_frame, 
            font=("Arial", 12),
            width=60
        )
        self.url_entry.pack(fill="x", padx=10, pady=10)
        self.url_entry.insert(0, "http://www.iyinghua.com/v/6543-1.html")
        
        # 按钮区域
        button_frame = tk.Frame(input_frame, bg="#f0f0f0")
        button_frame.pack(pady=5)
        
        self.parse_btn = tk.Button(
            button_frame,
            text="🔍 解析视频",
            command=self.start_parsing,
            bg="#667eea",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=5
        )
        self.parse_btn.pack(side="left", padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ 清空",
            command=self.clear_all,
            bg="#6c757d",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5
        )
        self.clear_btn.pack(side="left", padx=5)
        
        self.copy_btn = tk.Button(
            button_frame,
            text="📋 复制结果",
            command=self.copy_result,
            bg="#28a745",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5,
            state="disabled"
        )
        self.copy_btn.pack(side="left", padx=5)
        
        # 结果显示区域
        result_frame = tk.LabelFrame(
            self.root, 
            text="📊 解析结果", 
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        )
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            font=("Consolas", 10),
            height=15,
            wrap=tk.WORD
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 日志区域
        log_frame = tk.LabelFrame(
            self.root, 
            text="📝 解析日志", 
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        )
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            height=8,
            wrap=tk.WORD,
            bg="#2b2b2b",
            fg="#ffffff"
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=5)
        
    def log_message(self, message, level="INFO"):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "INFO": "#00ff00",
            "WARNING": "#ffff00", 
            "ERROR": "#ff0000",
            "SUCCESS": "#00ff00"
        }
        
        self.log_text.insert(tk.END, f"[{timestamp}] [{level}] {message}\n")
        self.log_text.tag_add(level, f"{self.log_text.index(tk.END)}-2l", f"{self.log_text.index(tk.END)}-1l")
        self.log_text.tag_config(level, foreground=color_map.get(level, "#ffffff"))
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def setup_driver(self):
        """设置Selenium驱动"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.log_message("✅ Chrome驱动初始化成功", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Chrome驱动初始化失败: {str(e)}", "ERROR")
            return False
            
    def extract_video_url(self, html_content, page_url):
        """从HTML内容中提取视频URL"""
        self.log_message("🔍 开始提取视频URL...")
        
        try:
            # 1. 提取页面标题
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "未知视频"
            self.log_message(f"📄 页面标题: {title}")
            
            # 2. 提取集数信息
            episode_match = re.search(r'第(\d+)集', title)
            current_episode = int(episode_match.group(1)) if episode_match else 1
            self.log_message(f"🎯 当前集数: 第{current_episode}集")
            
            # 3. 提取视频URL - 多种策略
            video_url = None
            
            # 策略1: 直接提取tup格式URL
            tup_pattern = r'["\'](https?://tup\.iyinghua\.com/\?vid=https?://[^"\']+\.m3u8[^"\']*)["\']'
            matches = re.findall(tup_pattern, html_content)
            if matches:
                video_url = matches[0]
                self.log_message(f"✅ 找到tup格式URL: {video_url}")
            else:
                # 策略2: 提取vid参数并构造URL
                vid_pattern = r'["\']vid["\']:\s*["\'](https?://[^"\']+\.m3u8[^"\']*)["\']'
                vid_matches = re.findall(vid_pattern, html_content)
                if vid_matches:
                    video_url = f"https://tup.iyinghua.com/?vid={vid_matches[0]}"
                    self.log_message(f"✅ 构造tup格式URL: {video_url}")
                else:
                    # 策略3: 提取其他m3u8 URL
                    m3u8_patterns = [
                        r'["\'](https?://[^"\']*bf8bf\.com[^"\']*\.m3u8[^"\']*)["\']',
                        r'["\'](https?://[^"\']*\.m3u8[^"\']*)["\']'
                    ]
                    for pattern in m3u8_patterns:
                        matches = re.findall(pattern, html_content)
                        if matches:
                            video_url = f"https://tup.iyinghua.com/?vid={matches[0]}"
                            self.log_message(f"✅ 找到m3u8 URL: {video_url}")
                            break
            
            # 4. 计算总集数
            total_episodes = 12  # 默认值
            episode_list_pattern = r'共(\d+)集'
            total_match = re.search(episode_list_pattern, html_content)
            if total_match:
                total_episodes = int(total_match.group(1))
                self.log_message(f"📊 总集数: {total_episodes}")
            
            return {
                'video_url': video_url,
                'title': title,
                'current_episode': current_episode,
                'total_episodes': total_episodes,
                'source_url': page_url
            }
            
        except Exception as e:
            self.log_message(f"❌ 提取视频URL失败: {str(e)}", "ERROR")
            return {
                'video_url': None,
                'title': '解析失败',
                'current_episode': 1,
                'total_episodes': 1,
                'source_url': page_url,
                'error': str(e)
            }
            
    def parse_video_url(self, url):
        """解析视频URL"""
        self.log_message(f"🚀 开始解析URL: {url}")
        
        try:
            # 验证URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                self.log_message("❌ 无效的URL格式", "ERROR")
                return None
                
            # 设置Selenium驱动
            if not self.setup_driver():
                return None
                
            self.log_message("🌐 正在访问页面...")
            self.driver.get(url)
            
            # 等待页面加载
            self.log_message("⏳ 等待页面加载...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 获取页面内容
            html_content = self.driver.page_source
            self.log_message("📄 获取页面内容成功")
            
            # 提取视频信息
            result = self.extract_video_url(html_content, url)
            
            return result
            
        except Exception as e:
            self.log_message(f"❌ 解析失败: {str(e)}", "ERROR")
            return None
            
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.log_message("🔒 Chrome驱动已关闭")
                
    def start_parsing(self):
        """开始解析"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入有效的URL")
            return
            
        # 禁用按钮，显示进度
        self.parse_btn.config(state="disabled")
        self.progress.start()
        
        # 清空之前的结果
        self.result_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        
        # 在新线程中执行解析
        thread = threading.Thread(target=self.parse_in_background, args=(url,))
        thread.daemon = True
        thread.start()
        
    def parse_in_background(self, url):
        """后台解析"""
        try:
            result = self.parse_video_url(url)
            
            if result:
                # 格式化结果显示
                formatted_result = f"""
🌸 解析结果详情
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 视频标题: {result['title']}
🎯 当前集数: 第 {result['current_episode']} 集
📊 总集数: {result['total_episodes']} 集
🔗 原始URL: {result['source_url']}
🎬 真实视频URL: {result['video_url'] or '未找到'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎬 可直接播放的URL:
{result['video_url'] or '使用备用测试视频: https://www.w3schools.com/html/mov_bbb.mp4'}
                """
                
                self.result_text.insert(tk.END, formatted_result)
                self.copy_btn.config(state="normal")
                
                if result['video_url']:
                    self.log_message("✅ 解析完成！真实视频URL已找到", "SUCCESS")
                else:
                    self.log_message("⚠️ 解析完成，但未找到真实视频URL", "WARNING")
            else:
                self.result_text.insert(tk.END, "❌ 解析失败，请检查日志")
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
            messagebox.showinfo("成功", "结果已复制到剪贴板")
            
    def run(self):
        """运行应用"""
        self.log_message("🌸 樱花动漫视频解析器已启动")
        self.log_message("💡 请输入樱花动漫页面URL，然后点击解析按钮")
        self.root.mainloop()

if __name__ == "__main__":
    # 检查必要的库
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
    except ImportError:
        print("❌ 请先安装必要的库:")
        print("pip install selenium beautifulsoup4 requests")
        sys.exit(1)
        
    app = VideoParserGUI()
    app.run()