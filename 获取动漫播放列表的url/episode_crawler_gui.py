#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫分集URL爬虫 - 可视化版本
专门爬取动漫详情页的分集列表，生成完整URL
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import requests
from bs4 import BeautifulSoup
import re
import json
import os
import threading
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

class EpisodeCrawlerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌸 樱花动漫分集URL爬虫")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f8f9fa')
        
        self.base_url = "http://www.iyinghua.com"
        self.episodes_data = []
        self.setup_ui()
        
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
            text="🌸 樱花动漫分集URL爬虫", 
            font=("Microsoft YaHei", 20, "bold"),
            fg="#2c3e50",
            bg="#f8f9fa"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="🔗 动漫页面URL输入", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        
        # URL输入框
        self.url_entry = ttk.Entry(input_frame, font=("Consolas", 11), width=60)
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.url_entry.insert(0, "http://www.iyinghua.com/show/6556.html")
        
        # 按钮区域
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=1)
        
        self.crawl_btn = ttk.Button(
            button_frame,
            text="🕷️ 开始爬取",
            command=self.start_crawling,
            style='Primary.TButton'
        )
        self.crawl_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="🗑️ 清空",
            command=self.clear_all
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.export_btn = ttk.Button(
            button_frame,
            text="📥 导出",
            command=self.export_data,
            state="disabled"
        )
        self.export_btn.pack(side=tk.LEFT)
        
        # 信息显示区域
        info_frame = ttk.LabelFrame(main_frame, text="📊 动漫信息", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 信息标签
        self.title_label = ttk.Label(info_frame, text="动漫标题: -", font=("Microsoft YaHei", 12, "bold"))
        self.title_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.episodes_label = ttk.Label(info_frame, text="总集数: -", font=("Microsoft YaHei", 11))
        self.episodes_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.url_label = ttk.Label(info_frame, text="页面URL: -", font=("Microsoft YaHei", 10))
        self.url_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # 结果表格
        table_frame = ttk.LabelFrame(main_frame, text="📋 分集列表", padding="10")
        table_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ("集数", "标题", "完整URL")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        # 设置列宽和对齐方式
        self.tree.heading("集数", text="集数")
        self.tree.heading("标题", text="标题")
        self.tree.heading("完整URL", text="完整URL")
        
        self.tree.column("集数", width=80, anchor=tk.CENTER)
        self.tree.column("标题", width=120, anchor=tk.W)
        self.tree.column("完整URL", width=600, anchor=tk.W)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="📝 爬取日志", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            height=6,
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
        self.progress.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        # 配置权重
        main_frame.rowconfigure(3, weight=2)
        main_frame.rowconfigure(4, weight=1)
        
        # 设置样式
        style = ttk.Style()
        style.configure('Primary.TButton', background='#007bff', foreground='white')
        
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
        
    def validate_url(self, url):
        """验证URL格式"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            if 'iyinghua.com' not in parsed.netloc:
                return False
            if not parsed.path.startswith('/show/'):
                return False
            return True
        except:
            return False
            
    def extract_anime_info(self, soup):
        """提取动漫基本信息"""
        try:
            # 提取标题
            title = "未知动漫"
            title_elem = soup.find('h1')
            if title_elem:
                title = title_elem.get_text().strip()
            else:
                title_elem = soup.find('title')
                if title_elem:
                    title = title_elem.get_text().strip()
                    # 清理标题
                    title = re.sub(r'[|_-].*', '', title).strip()
            
            return title
        except Exception as e:
            self.log_message(f"提取动漫信息失败: {str(e)}", "ERROR")
            return "未知动漫"
            
    def extract_episodes(self, soup):
        """提取分集信息"""
        episodes = []
        try:
            # 查找分集列表
            movurl_div = soup.find('div', class_='movurl')
            if not movurl_div:
                # 尝试其他可能的选择器
                movurl_div = soup.find('div', id='main0')
                if not movurl_div:
                    movurl_div = soup
            
            # 查找所有链接
            links = movurl_div.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '').strip()
                title = link.get_text().strip()
                
                # 验证链接格式
                if href and re.match(r'/v/\d+-\d+\.html', href):
                    full_url = urljoin(self.base_url, href)
                    
                    # 提取集数
                    episode_match = re.search(r'-(\d+)\.html', href)
                    episode_num = int(episode_match.group(1)) if episode_match else 0
                    
                    episodes.append({
                        'episode': episode_num,
                        'title': title,
                        'url': full_url,
                        'relative_url': href
                    })
            
            # 按集数排序
            episodes.sort(key=lambda x: x['episode'])
            return episodes
            
        except Exception as e:
            self.log_message(f"提取分集信息失败: {str(e)}", "ERROR")
            return []
            
    def crawl_episodes(self, url):
        """爬取分集信息"""
        self.log_message(f"🚀 开始爬取: {url}")
        
        try:
            # 验证URL
            if not self.validate_url(url):
                self.log_message("❌ 无效的动漫页面URL", "ERROR")
                return False
                
            # 设置请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
            
            self.log_message("🌐 发送请求...")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            self.log_message(f"✅ 获取页面成功 ({len(response.text)} 字符)")
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取信息
            anime_title = self.extract_anime_info(soup)
            episodes = self.extract_episodes(soup)
            
            if not episodes:
                self.log_message("⚠️ 未找到分集信息，尝试其他选择器...", "WARNING")
                # 尝试更广泛的搜索
                all_links = soup.find_all('a', href=re.compile(r'/v/\d+-\d+\.html'))
                for link in all_links:
                    href = link.get('href', '').strip()
                    title = link.get_text().strip()
                    if href:
                        full_url = urljoin(self.base_url, href)
                        episode_match = re.search(r'-(\d+)\.html', href)
                        episode_num = int(episode_match.group(1)) if episode_match else 0
                        episodes.append({
                            'episode': episode_num,
                            'title': title,
                            'url': full_url,
                            'relative_url': href
                        })
                
                episodes.sort(key=lambda x: x['episode'])
            
            # 更新UI
            self.title_label.config(text=f"动漫标题: {anime_title}")
            self.episodes_label.config(text=f"总集数: {len(episodes)}")
            self.url_label.config(text=f"页面URL: {url}")
            
            # 更新表格
            self.update_episodes_table(episodes)
            
            self.episodes_data = episodes
            self.export_btn.config(state="normal")
            
            self.log_message(f"✅ 爬取完成！共找到 {len(episodes)} 集", "SUCCESS")
            return True
            
        except requests.RequestException as e:
            self.log_message(f"❌ 网络请求失败: {str(e)}", "ERROR")
            return False
        except Exception as e:
            self.log_message(f"❌ 爬取失败: {str(e)}", "ERROR")
            return False
            
    def update_episodes_table(self, episodes):
        """更新分集表格"""
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 添加数据
        for ep in episodes:
            self.tree.insert('', 'end', values=(
                ep['episode'],
                ep['title'],
                ep['url']
            ))
            
    def start_crawling(self):
        """开始爬取"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入动漫页面URL")
            return
            
        # 禁用按钮，显示进度
        self.crawl_btn.config(state="disabled")
        self.export_btn.config(state="disabled")
        self.progress.start()
        
        # 清空之前的数据
        self.clear_all()
        
        # 在新线程中执行爬取
        thread = threading.Thread(target=self.crawl_in_background, args=(url,))
        thread.daemon = True
        thread.start()
        
    def crawl_in_background(self, url):
        """后台爬取"""
        try:
            success = self.crawl_episodes(url)
            
            if success and self.episodes_data:
                messagebox.showinfo("成功", f"爬取完成！共找到 {len(self.episodes_data)} 集")
            elif success:
                messagebox.showwarning("提示", "爬取完成，但未找到分集信息")
            else:
                messagebox.showerror("错误", "爬取失败，请查看日志")
                
        except Exception as e:
            self.log_message(f"后台任务错误: {str(e)}", "ERROR")
            messagebox.showerror("错误", f"爬取过程中发生错误: {str(e)}")
            
        finally:
            # 恢复按钮状态
            self.crawl_btn.config(state="normal")
            self.progress.stop()
            
    def export_data(self):
        """导出数据"""
        if not self.episodes_data:
            messagebox.showwarning("警告", "没有可导出的数据")
            return
            
        # 获取动漫标题
        anime_title = self.title_label.cget('text').replace("动漫标题: ", "")
        if anime_title == "-":
            anime_title = "未知动漫"
            
        # 选择导出格式
        file_types = [
            ("JSON文件", "*.json"),
            ("文本文件", "*.txt"),
            ("CSV文件", "*.csv")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="导出分集数据",
            initialfile=f"{anime_title}_episodes",
            filetypes=file_types,
            defaultextension=".json"
        )
        
        if not filename:
            return
            
        try:
            if filename.endswith('.json'):
                self.export_json(filename, anime_title)
            elif filename.endswith('.txt'):
                self.export_txt(filename, anime_title)
            elif filename.endswith('.csv'):
                self.export_csv(filename, anime_title)
                
            messagebox.showinfo("成功", f"数据已导出到: {filename}")
            self.log_message(f"📥 数据导出成功: {filename}", "SUCCESS")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            self.log_message(f"❌ 导出失败: {str(e)}", "ERROR")
            
    def export_json(self, filename, anime_title):
        """导出JSON格式"""
        export_data = {
            "anime_name": anime_title,
            "total_episodes": len(self.episodes_data),
            "base_url": self.base_url,
            "crawl_time": datetime.now().isoformat(),
            "episodes": self.episodes_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
            
    def export_txt(self, filename, anime_title):
        """导出文本格式"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"🌸 樱花动漫分集URL列表\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"动漫名称: {anime_title}\n")
            f.write(f"总集数: {len(self.episodes_data)}\n")
            f.write(f"爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"来源网站: {self.base_url}\n\n")
            f.write(f"{'='*50}\n\n")
            
            for ep in self.episodes_data:
                f.write(f"第{ep['episode']:02d}集: {ep['url']}\n")
                
    def export_csv(self, filename, anime_title):
        """导出CSV格式"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['集数', '标题', '完整URL', '相对URL'])
            
            for ep in self.episodes_data:
                writer.writerow([ep['episode'], ep['title'], ep['url'], ep['relative_url']])
                
    def clear_all(self):
        """清空所有内容"""
        self.title_label.config(text="动漫标题: -")
        self.episodes_label.config(text="总集数: -")
        self.url_label.config(text="页面URL: -")
        
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.log_text.delete(1.0, tk.END)
        self.episodes_data = []
        self.export_btn.config(state="disabled")
        
    def run(self):
        """运行应用"""
        self.log_message("🌸 樱花动漫分集URL爬虫已启动")
        self.log_message("💡 请输入动漫详情页URL，如: http://www.iyinghua.com/show/6556.html")
        self.log_message("📖 程序将自动提取所有分集的完整播放URL")
        self.root.mainloop()

if __name__ == "__main__":
    # 检查依赖
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
        
    app = EpisodeCrawlerGUI()
    app.run()