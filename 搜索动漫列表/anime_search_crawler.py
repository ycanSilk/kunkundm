#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫搜索爬虫 - 可视化版本
支持搜索动漫并获取列表数据，保存为JSON格式
"""

import requests
from bs4 import BeautifulSoup
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import urllib.parse
import os
from datetime import datetime
import re

class AnimeSearchCrawler:
    def __init__(self):
        self.base_url = "http://www.iyinghua.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def search_anime(self, keyword):
        """搜索动漫"""
        try:
            # URL编码关键词
            encoded_keyword = urllib.parse.quote(keyword)
            search_url = f"{self.base_url}/search/{encoded_keyword}/"
            
            print(f"🌸 正在搜索: {keyword}")
            print(f"🔗 URL: {search_url}")
            
            response = requests.get(search_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            return self.parse_search_results(response.text, keyword)
            
        except requests.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except Exception as e:
            raise Exception(f"搜索失败: {str(e)}")

    def parse_search_results(self, html_content, keyword):
        """解析搜索结果"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # 查找搜索结果列表
        lpic_div = soup.find('div', class_='lpic')
        if not lpic_div:
            return results
            
        anime_items = lpic_div.find_all('li')
        
        for item in anime_items:
            try:
                # 提取动漫信息
                anime_data = {}
                
                # 图片URL和alt文本
                img_tag = item.find('img')
                if img_tag:
                    anime_data['image_url'] = img_tag.get('src', '')
                    anime_data['alt_text'] = img_tag.get('alt', '')
                
                # 标题和链接
                title_link = item.find('h2').find('a') if item.find('h2') else None
                if title_link:
                    anime_data['title'] = title_link.get_text(strip=True)
                    anime_data['detail_url'] = urllib.parse.urljoin(self.base_url, title_link.get('href', ''))
                    anime_data['detail_path'] = title_link.get('href', '')
                
                # 直接获取真实的集数标签内容 - 原样提取，不做任何判断
                episodes_text = "未知"
                spans = item.find_all('span')
                if spans:
                    # 直接获取第一个span的完整文本内容
                    episodes_text = spans[0].get_text(strip=True)
                anime_data['episodes_raw'] = episodes_text
                
                # 类型信息 - 基于实际HTML结构修复
                anime_data['genres'] = []
                # 查找包含"类型："的span标签
                spans = item.find_all('span')
                for span in spans:
                    text = span.get_text(strip=True)
                    if '类型：' in text:
                        # 提取span内的所有a标签作为类型
                        type_links = span.find_all('a')
                        if type_links:
                            anime_data['genres'] = [a.get_text(strip=True) for a in type_links]
                        else:
                            # 如果没有a标签，从文本中提取类型
                            type_text = text.replace('类型：', '').strip()
                            # 按常见类型分割
                            types = []
                            for t in ['搞笑', '冒险', '校园', '日常', '奇幻', '百合', '战斗', '热血', '科幻', '恋爱']:
                                if t in type_text:
                                    types.append(t)
                            if types:
                                anime_data['genres'] = types
                            else:
                                anime_data['genres'] = [type_text] if type_text else []
                        break
                
                # 详细描述
                desc_p = item.find('p')
                if desc_p:
                    anime_data['description'] = desc_p.get_text(strip=True)
                else:
                    anime_data['description'] = "暂无描述"
                
                # 搜索关键词和时间
                anime_data['search_keyword'] = keyword
                anime_data['search_time'] = datetime.now().isoformat()
                
                if anime_data.get('title'):  # 确保有标题才添加
                    results.append(anime_data)
                    
            except Exception as e:
                print(f"解析单个动漫信息失败: {str(e)}")
                continue
        
        return results

class AnimeSearchGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌸 樱花动漫搜索工具")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")
        
        self.crawler = AnimeSearchCrawler()
        self.search_results = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg="#ff6b6b", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🌸 樱花动漫搜索工具", 
                              font=("Microsoft YaHei", 20, "bold"), fg="white", bg="#ff6b6b")
        title_label.pack(pady=20)
        
        # 搜索区域
        search_frame = tk.Frame(self.root, bg="#f5f5f5", pady=20)
        search_frame.pack(fill=tk.X)
        
        tk.Label(search_frame, text="搜索关键词:", font=("Microsoft YaHei", 12)).pack(side=tk.LEFT, padx=10)
        
        self.search_entry = tk.Entry(search_frame, font=("Microsoft YaHei", 12), width=40)
        self.search_entry.pack(side=tk.LEFT, padx=10)
        self.search_entry.bind("<Return>", lambda e: self.start_search())
        
        self.search_btn = tk.Button(search_frame, text="🔍 搜索", command=self.start_search,
                                   font=("Microsoft YaHei", 12), bg="#ff6b6b", fg="white")
        self.search_btn.pack(side=tk.LEFT, padx=10)
        
        self.clear_btn = tk.Button(search_frame, text="清空", command=self.clear_results,
                                 font=("Microsoft YaHei", 12), bg="#6c757d", fg="white")
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 加载图片相关
        try:
            from PIL import Image, ImageTk
            import requests
            from io import BytesIO
            self.Image = Image
            self.ImageTk = ImageTk
            self.requests = requests
            self.BytesIO = BytesIO
            self.image_support = True
        except ImportError:
            self.image_support = False
        
        # 结果统计
        self.result_label = tk.Label(self.root, text="暂无搜索结果", 
                                   font=("Microsoft YaHei", 10), bg="#f5f5f5")
        self.result_label.pack(pady=5)
        
        # 创建主框架
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建主框架 - 改为左右布局
        left_frame = tk.Frame(main_frame, bg="#f5f5f5")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(main_frame, bg="#f5f5f5", width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # 创建Treeview - 放在左侧
        columns = ("标题", "集数", "类型")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="tree headings", height=15)
        
        # 设置列宽和对齐
        self.tree.heading("#0", text="")
        self.tree.heading("标题", text="动漫标题")
        self.tree.heading("集数", text="集数")
        self.tree.heading("类型", text="类型")
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("标题", width=250, anchor=tk.W)
        self.tree.column("集数", width=100, anchor=tk.CENTER)
        self.tree.column("类型", width=150, anchor=tk.CENTER)
        
        # 右侧详情面板
        detail_label = tk.Label(right_frame, text="动漫详情", font=("Microsoft YaHei", 14, "bold"), bg="#f5f5f5")
        detail_label.pack(pady=10)
        
        # 图片显示区域
        self.image_label = tk.Label(right_frame, text="暂无图片", bg="#e9ecef", 
                                   width=250, height=150, relief=tk.RAISED)
        self.image_label.pack(pady=5)
        
        # 详情文本区域
        self.detail_text = tk.Text(right_frame, height=15, width=35, font=("Microsoft YaHei", 10))
        self.detail_text.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # 滚动条
        detail_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=detail_scrollbar.set)
        detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定选择事件
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # 按钮区域
        button_frame = tk.Frame(self.root, bg="#f5f5f5", pady=10)
        button_frame.pack(fill=tk.X)
        
        self.export_btn = tk.Button(button_frame, text="💾 导出JSON", command=self.export_json,
                                   font=("Microsoft YaHei", 12), bg="#28a745", fg="white", state=tk.DISABLED)
        self.export_btn.pack(side=tk.LEFT, padx=20)
        
        self.copy_btn = tk.Button(button_frame, text="📋 复制链接", command=self.copy_selected_url,
                                font=("Microsoft YaHei", 12), bg="#007bff", fg="white", state=tk.DISABLED)
        self.copy_btn.pack(side=tk.LEFT, padx=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        
        # 状态栏
        self.status_bar = tk.Label(self.root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def start_search(self):
        """开始搜索"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入搜索关键词！")
            return
            
        # 禁用搜索按钮
        self.search_btn.config(state=tk.DISABLED)
        self.progress.pack(fill=tk.X, padx=20)
        self.progress.start()
        
        # 清空之前的结果
        self.clear_results()
        self.status_bar.config(text=f"正在搜索: {keyword}...")
        
        # 在新线程中执行搜索
        thread = threading.Thread(target=self.perform_search, args=(keyword,))
        thread.daemon = True
        thread.start()
    
    def perform_search(self, keyword):
        """执行搜索"""
        try:
            results = self.crawler.search_anime(keyword)
            
            self.root.after(0, self.update_results, results)
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
    
    def update_results(self, results):
        """更新搜索结果"""
        self.search_results = results
        
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 清空详情区域
        self.image_label.config(text="暂无图片", image="")
        self.detail_text.delete(1.0, tk.END)
        
        # 添加新结果
        for anime in results:
            genres = ", ".join(anime.get('genres', []))
            self.tree.insert("", tk.END, values=(
                anime.get('title', '未知标题'),
                anime.get('episodes_raw', '未知'),
                genres
            ))
        
        # 更新统计
        count = len(results)
        self.result_label.config(text=f"找到 {count} 个结果")
        self.status_bar.config(text=f"搜索完成，共找到 {count} 个动漫")
        
        # 启用按钮
        self.search_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.NORMAL if count > 0 else tk.DISABLED)
        self.copy_btn.config(state=tk.NORMAL if count > 0 else tk.DISABLED)
        
        self.progress.stop()
        self.progress.pack_forget()
    
    def show_error(self, error_msg):
        """显示错误"""
        messagebox.showerror("错误", error_msg)
        self.search_btn.config(state=tk.NORMAL)
        self.status_bar.config(text="搜索失败")
        self.progress.stop()
        self.progress.pack_forget()
    
    def clear_results(self):
        """清空结果"""
        self.search_results = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.result_label.config(text="暂无搜索结果")
        self.export_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.status_bar.config(text="已清空结果")
    
    def export_json(self):
        """导出JSON文件"""
        if not self.search_results:
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"anime_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.search_results, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", f"数据已导出到:\n{filename}")
                self.status_bar.config(text=f"已导出到: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("导出失败", str(e))
    
    def copy_selected_url(self):
        """复制选中项的URL"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要复制的项目")
            return
        
        item = selection[0]
        url = self.tree.item(item, 'values')[3]
        
        self.root.clipboard_clear()
        self.root.clipboard_append(url)
        messagebox.showinfo("成功", "链接已复制到剪贴板")
    
    def on_item_double_click(self, event):
        """双击打开详情页"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            index = self.tree.index(item)
            if index < len(self.search_results):
                url = self.search_results[index].get('detail_url', '')
                if url:
                    import webbrowser
                    webbrowser.open(url)

    def on_item_select(self, event):
        """选择项目时显示详情"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            index = self.tree.index(item)
            if index < len(self.search_results):
                anime = self.search_results[index]
                self.display_anime_detail(anime)

    def display_anime_detail(self, anime):
        """显示动漫详情"""
        # 清空详情区域
        self.detail_text.delete(1.0, tk.END)
        
        # 显示图片
        self.display_image(anime.get('image_url', ''))
        
        # 显示详细信息
        detail_text = f"""
📺 动漫名称：
{anime.get('title', '未知')}

🎬 集数信息：
{anime.get('episodes_raw', '未知')}

🏷️ 类型标签：
{', '.join(anime.get('genres', [])) if anime.get('genres') else '未知'}

📝 详细描述：
{anime.get('description', '暂无描述')}

🔗 详情链接：
{anime.get('detail_url', '无')}
        """
        
        self.detail_text.insert(1.0, detail_text.strip())
        
        # 设置文本样式
        self.detail_text.tag_configure("bold", font=("Microsoft YaHei", 10, "bold"))
        self.detail_text.tag_configure("normal", font=("Microsoft YaHei", 10))
        
        # 高亮标题
        start_idx = self.detail_text.search("📺 动漫名称：", 1.0, tk.END)
        if start_idx:
            end_idx = f"{start_idx}+10c"
            self.detail_text.tag_add("bold", start_idx, end_idx)

    def display_image(self, image_url):
        """显示动漫图片"""
        if not image_url or not self.image_support:
            self.image_label.config(text="暂无图片", image="")
            return
            
        try:
            # 下载图片
            response = self.requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # 处理图片
            image_data = self.BytesIO(response.content)
            img = self.Image.open(image_data)
            
            # 调整图片大小以适应界面
            img = img.resize((250, 150), self.Image.Resampling.LANCZOS)
            photo = self.ImageTk.PhotoImage(img)
            
            # 显示图片
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo  # 保持引用
            
        except Exception as e:
            print(f"加载图片失败: {str(e)}")
            self.image_label.config(text="加载失败", image="")
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AnimeSearchGUI()
    app.run()