import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import threading
import json
import os
from urllib.parse import quote

class AnimeSearchTool:
    def __init__(self, root):
        self.root = root
        self.root.title("动漫视频搜索工具")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 浏览器驱动实例
        self.driver = None
        self.is_running = False
        
        # 创建界面
        self.create_widgets()
        
        # 加载配置
        self.load_config()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="动漫视频搜索工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 搜索选项框架
        options_frame = ttk.LabelFrame(main_frame, text="搜索选项", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # 网站选择
        ttk.Label(options_frame, text="目标网站:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.site_var = tk.StringVar()
        sites = [
            "https://www.agemys.org/",
            "https://www.bimiacg4.net/", 
            "https://www.yhdmp.cc/",
            "http://m.iyinghua.com/"  # 樱花动漫移动版
        ]
        self.site_combo = ttk.Combobox(options_frame, textvariable=self.site_var, values=sites, width=50)
        self.site_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        self.site_combo.current(3)  # 默认选择樱花动漫移动版
        
        # 动漫名称输入
        ttk.Label(options_frame, text="动漫名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.anime_var = tk.StringVar()
        anime_entry = ttk.Entry(options_frame, textvariable=self.anime_var, width=50)
        anime_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 延迟设置
        ttk.Label(options_frame, text="延迟(秒):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.delay_var = tk.StringVar(value="2")
        delay_entry = ttk.Entry(options_frame, textvariable=self.delay_var, width=10)
        delay_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # 控制按钮
        self.start_button = ttk.Button(button_frame, text="开始搜索", command=self.start_search)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="停止", command=self.stop_search, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # 浏览器选项
        browser_frame = ttk.Frame(button_frame)
        browser_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        ttk.Label(browser_frame, text="浏览器:").pack(side=tk.LEFT)
        self.browser_var = tk.StringVar(value="visible")
        ttk.Radiobutton(browser_frame, text="可见", variable=self.browser_var, value="visible").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Radiobutton(browser_frame, text="隐藏", variable=self.browser_var, value="hidden").pack(side=tk.LEFT)
        
        # 日志框架
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=80, height=15)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 结果框架
        result_frame = ttk.LabelFrame(main_frame, text="搜索结果", padding="10")
        result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=80, height=15)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
    
    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists("anime_sites.json"):
                with open("anime_sites.json", "r", encoding="utf-8") as f:
                    sites = json.load(f)
                    self.site_combo["values"] = sites
        except:
            pass
    
    def save_config(self):
        """保存配置"""
        try:
            sites = list(self.site_combo["values"])
            with open("anime_sites.json", "w", encoding="utf-8") as f:
                json.dump(sites, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.status_var.set(message)
    
    def clear_results(self):
        """清除结果"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def start_search(self):
        """开始搜索"""
        if self.is_running:
            return
        
        anime_name = self.anime_var.get().strip()
        if not anime_name:
            messagebox.showwarning("警告", "请输入动漫名称")
            return
        
        site_url = self.site_var.get().strip()
        if not site_url:
            messagebox.showwarning("警告", "请选择目标网站")
            return
        
        try:
            delay = float(self.delay_var.get())
        except:
            delay = 2.0
        
        # 更新UI状态
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 在后台线程中运行搜索
        thread = threading.Thread(target=self.run_search, args=(site_url, anime_name, delay))
        thread.daemon = True
        thread.start()
    
    def stop_search(self):
        """停止搜索"""
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_message("搜索已停止")
    
    def run_search(self, site_url, anime_name, delay):
        """执行搜索"""
        try:
            # 初始化浏览器
            chrome_options = Options()
            if self.browser_var.get() == "hidden":
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--window-size=1200,800")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # 自动下载和管理ChromeDriver
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except ImportError:
                # 如果webdriver_manager未安装，使用传统方式
                self.log_message("建议使用: pip install webdriver-manager 来自动管理ChromeDriver")
                self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.log_message(f"正在访问网站: {site_url}")
            self.driver.get(site_url)
            time.sleep(delay)
            
            # 不同的网站可能需要不同的选择器
            # 这里提供一些常见的选择器示例
            selectors = {
                "search_input": ["input[name='key']", "input[name='wd']", "input[type='text']", "#search-input", ".search-input"],
                "search_button": ["button[type='submit']", "input[type='submit']", ".search-btn", "#search-button"]
            }
            
            # 尝试查找搜索框
            search_input = None
            for selector in selectors["search_input"]:
                try:
                    search_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if search_input:
                        break
                except:
                    continue
            
            if not search_input:
                self.log_message("未找到搜索框，尝试通过URL直接搜索")
                # 使用正确的搜索URL格式
                if "agemys" in site_url:
                    search_url = f"https://www.agemys.org/search?query={quote(anime_name)}"
                elif "bimiacg" in site_url:
                    search_url = f"https://www.bimiacg4.net/vod/search/{quote(anime_name)}.html"
                elif "yhdmp" in site_url or "iyinghua" in site_url:
                    # 使用樱花动漫移动版的正确搜索URL格式
                    search_url = f"http://m.iyinghua.com/search/{quote(anime_name)}/"
                else:
                    search_url = f"{site_url}search?q={quote(anime_name)}"
                
                self.driver.get(search_url)
                time.sleep(delay)
            else:
                # 找到搜索框，输入关键词并搜索
                self.log_message("找到搜索框，输入关键词")
                search_input.clear()
                search_input.send_keys(anime_name)
                time.sleep(1)
                
                # 尝试查找搜索按钮
                search_button = None
                for selector in selectors["search_button"]:
                    try:
                        search_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if search_button:
                            break
                    except:
                        continue
                
                if search_button:
                    search_button.click()
                else:
                    search_input.send_keys(Keys.RETURN)
                
                time.sleep(delay)
            
            # 获取页面内容并解析结果
            self.log_message("正在解析搜索结果...")
            page_source = self.driver.page_source
            
            # 解析搜索结果
            results = self.parse_search_results(page_source, site_url)
            
            # 显示结果
            self.show_results(results, anime_name)
            
            self.log_message("搜索完成")
            
        except Exception as e:
            self.log_message(f"发生错误: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
            
            self.is_running = False
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
    
    def parse_search_results(self, page_source, site_url):
        """解析搜索结果"""
        # 这里需要根据不同的网站编写不同的解析逻辑
        # 以下是一些示例选择器
        
        results = []
        
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 根据不同网站使用不同的选择器
            if "agemys" in site_url:
                # 年龄动漫网的解析逻辑
                items = soup.select('.card .card-body .card-text')
                for item in items:
                    try:
                        title_elem = item.select_one('a')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href')
                            if link and not link.startswith('http'):
                                link = 'https://www.agemys.org' + link
                            results.append({"title": title, "url": link})
                    except:
                        continue
            
            elif "bimiacg" in site_url:
                # 哔咪动漫的解析逻辑
                items = soup.select('.module-card-item')
                for item in items:
                    try:
                        title_elem = item.select_one('.module-card-item-title a')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href')
                            if link and not link.startswith('http'):
                                link = 'https://www.bimiacg4.net' + link
                            results.append({"title": title, "url": link})
                    except:
                        continue
            
            elif "yhdmp" in site_url:
                # 樱花动漫的解析逻辑
                items = soup.select('.lpic li')
                for item in items:
                    try:
                        title_elem = item.select_one('h2 a')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            link = title_elem.get('href')
                            if link and not link.startswith('http'):
                                link = 'https://www.yhdmp.cc' + link
                            results.append({"title": title, "url": link})
                    except:
                        continue
            
            else:
                # 通用解析逻辑
                # 尝试查找可能的搜索结果元素
                selectors = [
                    '.result-item', '.search-result', '.item', '.video-item',
                    'h3 a', '.title a', '.name a', 'a[href*="video"]'
                ]
                
                for selector in selectors:
                    items = soup.select(selector)
                    if items:
                        for item in items:
                            try:
                                title = item.get_text(strip=True)
                                link = item.get('href')
                                if link and title and len(title) > 5:
                                    if link and not link.startswith('http'):
                                        link = site_url + link if site_url.endswith('/') else site_url + '/' + link
                                    results.append({"title": title, "url": link})
                            except:
                                continue
        
        except Exception as e:
            self.log_message(f"解析结果时出错: {str(e)}")
        
        return results
    
    def show_results(self, results, anime_name):
        """显示搜索结果"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        if results:
            self.result_text.insert(tk.END, f"找到 {len(results)} 个与 '{anime_name}' 相关的结果:\n\n")
            for i, result in enumerate(results, 1):
                self.result_text.insert(tk.END, f"{i}. {result['title']}\n")
                self.result_text.insert(tk.END, f"   链接: {result['url']}\n\n")
        else:
            self.result_text.insert(tk.END, f"未找到与 '{anime_name}' 相关的结果\n")
            self.result_text.insert(tk.END, "尝试使用不同的关键词或网站")
        
        self.result_text.config(state=tk.DISABLED)
    
    def on_closing(self):
        """程序关闭时的处理"""
        self.stop_search()
        self.save_config()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimeSearchTool(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()