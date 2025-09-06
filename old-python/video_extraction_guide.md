# 樱花动漫真实视频链接提取指南

## 📋 概述

本指南教你如何从樱花动漫网站提取真实的视频链接（m3u8/mp4格式），绕过网站的反爬虫机制。

## 🛠️ 工具介绍

### 1. 基础提取器 (`video_link_extractor.py`)
- ✅ 支持m3u8和mp4格式
- ✅ 自动检测视频质量
- ✅ 验证链接有效性
- ✅ 简单易用

### 2. 高级提取器 (`advanced_video_extractor.py`)
- ✅ 支持加密视频源解析
- ✅ 整剧批量提取
- ✅ 多种提取方法
- ✅ 自动生成下载选项
- ✅ 支持ffmpeg下载

## 🚀 使用方法

### 📥 安装依赖

```bash
pip install selenium beautifulsoup4 requests webdriver-manager
```

### 📺 提取单集视频

#### 方法1: 基础提取器
```bash
python video_link_extractor.py http://www.iyinghua.com/v/6543-1.html
```

#### 方法2: 高级提取器（推荐）
```bash
python advanced_video_extractor.py http://www.iyinghua.com/v/6543-1.html
```

### 📺 提取整剧信息

```bash
python advanced_video_extractor.py --series http://www.iyinghua.com/v/6543/
```

## 🔍 技术原理

### 1. 视频链接类型

| 类型 | 格式 | 特点 | 提取方法 |
|---|---|---|---|
| **m3u8** | `.m3u8` | 分段视频流，支持多清晰度 | 网络请求拦截 |
| **mp4** | `.mp4` | 完整视频文件 | 直接URL提取 |
| **加密m3u8** | `.m3u8` | 需要密钥解密 | 配置解析 |

### 2. 提取策略

#### 🎯 直接提取
- 从`<video>`标签的`src`属性
- 从`<source>`标签的`src`属性

#### 🔍 配置解析
- 解析JavaScript播放器配置
- 提取加密配置中的URL
- 解码Base64编码的链接

#### 🕵️ 网络拦截
- 使用浏览器开发者工具
- 拦截XHR/fetch请求
- 提取真实的m3u8请求

### 3. 反反爬虫技术

#### 🛡️ 浏览器伪装
```python
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
```

#### ⏱️ 智能等待
- 动态内容加载等待
- AJAX请求完成检测
- 超时重试机制

#### 🔄 请求头伪装
- 真实User-Agent
- 正确的Referer
- 浏览器指纹模拟

## 📊 输出格式

### 单集提取结果
```json
{
  "success": true,
  "video_info": {
    "title": "动漫标题",
    "episode": "1",
    "anime_id": "6543"
  },
  "sources": [
    {
      "type": "m3u8",
      "url": "https://video.iyinghua.com/xxx.m3u8",
      "quality": "720p",
      "file_size": 1024000
    }
  ],
  "download_options": [
    {
      "quality": "720p",
      "url": "https://video.iyinghua.com/xxx.m3u8",
      "filename": "video_720p.m3u8"
    }
  ]
}
```

### 整剧提取结果
```json
{
  "title": "动漫标题",
  "total_episodes": 12,
  "episodes": [
    {
      "episode": 1,
      "url": "http://www.iyinghua.com/v/6543-1.html",
      "title": "第1集"
    }
  ]
}
```

## 🎬 下载视频

### 使用ffmpeg下载m3u8
```bash
# 安装ffmpeg
# Windows: 下载ffmpeg.exe并添加到PATH
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg

# 下载m3u8视频
ffmpeg -i "https://video.iyinghua.com/xxx.m3u8" -c copy output.mp4
```

### 使用工具自动下载
```python
from advanced_video_extractor import AdvancedYinghuaExtractor

extractor = AdvancedYinghuaExtractor()
result = extractor.extract_real_video_links(url)

# 使用ffmpeg下载
success, message = extractor.download_with_ffmpeg(
    result['sources'][0]['url'], 
    "output.mp4"
)
```

## ⚠️ 注意事项

### 🚨 法律声明
- **仅限个人学习使用**
- **不得用于商业用途**
- **遵守版权法规**
- **尊重网站robots.txt**

### 🔧 技术限制
- 部分视频可能有DRM保护
- 某些链接可能有时效性
- 高并发可能导致IP封禁
- 需要处理验证码

### 💡 最佳实践
1. **合理设置延迟** - 避免过快请求
2. **使用代理** - 防止IP封禁
3. **缓存结果** - 避免重复提取
4. **错误处理** - 完善的异常捕获

## 🐛 常见问题

### Q: 提取不到视频链接
**A:** 可能原因：
- 页面加载不完整，增加等待时间
- 视频需要登录权限
- 反爬虫机制触发，使用代理

### Q: m3u8链接无效
**A:** 解决方案：
- 检查链接是否过期
- 验证Referer是否正确
- 使用浏览器直接访问测试

### Q: 下载速度慢
**A:** 优化方法：
- 选择更近的CDN节点
- 使用多线程下载工具
- 避开网络高峰期

### Q: 如何处理加密m3u8
**A:** 需要额外步骤：
- 提取解密密钥
- 下载密钥文件
- 使用ffmpeg解密下载

## 📞 技术支持

如遇到问题，请检查：
1. ChromeDriver版本是否匹配
2. 网络连接是否正常
3. 页面URL是否正确
4. 是否有最新反爬虫更新

## 🔄 更新日志

- **v1.0.0** - 基础视频链接提取
- **v1.1.0** - 支持加密视频源
- **v1.2.0** - 添加整剧批量提取
- **v1.3.0** - 集成ffmpeg下载功能