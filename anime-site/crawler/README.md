# 动漫爬虫系统

## 🎯 功能概述

这个爬虫系统专为anime-site项目设计，用于从各大动漫网站爬取数据并发送到Next.js后端API。

## 📁 项目结构

```
crawler/
├── anime_crawler.py      # 主爬虫类
├── run_crawler.py        # 启动脚本
├── config.py            # 配置文件
├── requirements.txt     # Python依赖
├── .env.example        # 环境变量模板
└── README.md           # 本文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入爬虫目录
cd crawler/

# 安装Python依赖
pip install -r requirements.txt

# 复制环境变量模板
cp .env.example .env

# 编辑配置文件
vim .env
```

### 2. 测试连接

```bash
# 确保Next.js服务正在运行
npm run dev

# 测试爬虫连接
python run_crawler.py --action test
```

### 3. 爬取模拟数据

```bash
# 爬取20条模拟数据
python run_crawler.py --action crawl --count 20

# 指定API地址
python run_crawler.py --api-url http://localhost:3000 --count 50
```

## 📋 API端点

### 接收数据
- **POST /api/crawler** - 接收爬虫数据
- **POST /api/anime** - 接收动漫数据

### 获取数据
- **GET /api/anime?action=list** - 获取动漫列表
- **GET /api/anime?action=weekly** - 获取每周更新
- **GET /api/anime?action=search&q=关键词** - 搜索动漫

## 🔄 数据格式

### 动漫列表数据
```json
{
  "crawler_type": "anime_list",
  "data": [
    {
      "id": "1",
      "title": "动漫名称",
      "coverImage": "https://example.com/cover.jpg",
      "episodes": 12,
      "currentEpisode": 8,
      "genre": ["奇幻", "冒险"],
      "description": "动漫简介",
      "year": 2024,
      "rating": 8.5
    }
  ]
}
```

### 每周更新数据
```json
{
  "crawler_type": "weekly_updates",
  "data": {
    "周一": [
      {
        "id": "anime_1",
        "title": "动漫名称",
        "episode": 9,
        "coverImage": "https://example.com/cover.jpg"
      }
    ]
  }
}
```

## ⚙️ 配置说明

### 环境变量 (.env)
```bash
# API配置
API_BASE_URL=http://localhost:3000

# 数据源
YHDM_BASE_URL=https://www.yhdm.tv
AGEFANS_BASE_URL=https://www.agefans.cc

# 爬虫参数
CRAWLER_DELAY=1.0
MAX_RETRIES=3
REQUEST_TIMEOUT=10
```

### 爬虫配置 (config.py)
- `REQUEST_DELAY`: 请求间隔时间(秒)
- `MAX_RETRIES`: 最大重试次数
- `REQUEST_TIMEOUT`: 请求超时时间(秒)
- `MAX_CONCURRENT`: 最大并发数

## 🔧 扩展开发

### 添加新的数据源

1. 在 `config.py` 的 `DATA_SOURCES` 中添加新配置
2. 创建对应的爬虫类继承 `AnimeCrawler`
3. 在 `run_crawler.py` 中添加新的爬虫类型

### 示例：创建真实爬虫

```python
from anime_crawler import AnimeCrawler
import requests
from bs4 import BeautifulSoup

class RealAnimeCrawler(AnimeCrawler):
    def crawl_yhdm_list(self):
        """爬取樱花动漫列表"""
        url = "https://www.yhdm.tv/list/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 解析数据逻辑...
        anime_list = []
        # 添加到anime_list...
        
        return self.send_data("anime_list", anime_list, url)
```

## 🐛 故障排除

### 常见问题

1. **连接失败**
   - 检查Next.js服务是否运行
   - 确认API地址正确
   - 检查防火墙设置

2. **数据格式错误**
   - 验证JSON格式
   - 检查必需字段
   - 查看API响应

3. **爬虫被封**
   - 增加请求延迟
   - 使用代理IP
   - 更换User-Agent

## 📊 监控和日志

- 日志文件：`crawler.log`
- 实时监控：`tail -f crawler.log`
- 错误统计：查看日志中的ERROR级别

## 📝 注意事项

- 请遵守目标网站的robots.txt规则
- 合理设置请求间隔，避免对目标网站造成压力
- 生产环境建议使用数据库存储数据
- 定期清理日志文件避免过大