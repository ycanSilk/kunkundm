# 樱花动漫最新更新爬虫

## 功能说明
这个爬虫用于爬取樱花动漫首页的最新更新部分内容，使用指定的CSS选择器`body .area div .img ul li`提取所有内容。

## 文件结构
```
最新更新/
├── latest_update_crawler.py    # 主爬虫脚本
├── requirements.txt           # 依赖文件
├── README.md                  # 使用说明
└── [生成的JSON文件]            # 爬取结果文件
```

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 直接运行
```bash
python latest_update_crawler.py
```

### 2. 作为模块调用
```python
from latest_update_crawler import LatestUpdateCrawler

crawler = LatestUpdateCrawler()
result = crawler.crawl_latest_updates()
print(result)
```

## 输出格式
爬取结果会保存为JSON文件，包含以下信息：
- `success`: 是否成功
- `total_count`: 总更新数量
- `data`: 更新列表，每个项目包含：
  - `title`: 动漫标题
  - `cover_image`: 封面图片URL
  - `detail_url`: 详情页URL
  - `episode_info`: 更新信息（如"更新至12集"）
  - `anime_type`: 动漫类型
  - `current_episode`: 当前集数（数字）
- `timestamp`: 爬取时间
- `source_url`: 来源URL

## 示例输出
```json
{
  "success": true,
  "total_count": 20,
  "data": [
    {
      "title": "鬼灭之刃 刀匠村篇",
      "cover_image": "//pic1.iqiyipic.com/image/20230418/...",
      "detail_url": "http://www.iyinghua.com/v/12345.html",
      "episode_info": "更新至11集",
      "current_episode": 11,
      "anime_type": "热血/战斗"
    }
  ],
  "timestamp": "2024-01-15T10:30:00",
  "source_url": "http://www.iyinghua.com"
}
```