# 最新更新API文档

## 概述

该API端点实现了调用Python爬虫获取樱花动漫最新更新，并将数据保存为JSON文件的功能。

## 端点信息

- **URL**: `/api/latest-update`
- **方法**: GET, POST
- **内容类型**: `application/json`

## 请求参数

### GET请求
```
GET /api/latest-update?real=true&limit=20&save=true
```

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `real` | boolean | false | 是否使用真实Python爬虫数据 |
| `limit` | number | 20 | 返回数据条数限制 |
| `save` | boolean | false | 是否将数据保存为JSON文件 |

### POST请求
```json
POST /api/latest-update
Content-Type: application/json

{
  "useRealData": true,
  "limit": 50,
  "saveToFile": true
}
```

## 响应格式

### 成功响应
```json
{
  "success": true,
  "data": [
    {
      "title": "百妖谱·洛阳篇",
      "cover_image": "http://css.yhdmtu.xyz/news/2023/10/07/da7f014187a0f.jpg",
      "detail_url": "http://www.iyinghua.com/show/6594.html",
      "episode_info": "更新至12集",
      "current_episode": 12
    }
  ],
  "total_count": 5,
  "timestamp": "2025-09-07T16:44:18.755Z",
  "source_url": "http://www.iyinghua.com",
  "filePath": "F:\\github\\kunkundm\\anime-site\\data\\latest_updates_2025-09-07_123456789.json"
}
```

### 错误响应
```json
{
  "success": false,
  "data": [],
  "total_count": 0,
  "timestamp": "2025-09-07T16:44:18.755Z",
  "source_url": "http://www.iyinghua.com",
  "error": "错误信息"
}
```

## 使用示例

### 1. 使用GET请求获取最新更新并保存文件
```bash
curl "http://localhost:3000/api/latest-update?real=true&limit=10&save=true"
```

### 2. 使用POST请求触发实时爬取
```bash
curl -X POST http://localhost:3000/api/latest-update \
  -H "Content-Type: application/json" \
  -d '{"useRealData": true, "limit": 20, "saveToFile": true}'
```

### 3. 使用模拟数据（不调用爬虫）
```bash
curl "http://localhost:3000/api/latest-update?limit=5"
```

## JSON文件保存

当 `save=true` 或 `saveToFile=true` 时，数据将保存到 `data/` 目录下的JSON文件：

- **文件名格式**: `latest_updates_YYYY-MM-DD_timestamp.json`
- **保存路径**: `anime-site/data/`
- **文件内容**: 包含完整的数据、统计信息和元数据

## 错误处理

- 如果Python爬虫失败，API会自动回退到模拟数据
- 所有错误都会记录在控制台
- 超时保护：Python爬虫最多运行15秒

## 注意事项

1. 确保Python环境已安装所需依赖：
   ```bash
   pip install -r src/app/python/requirements.txt
   ```

2. 确保Python可执行文件在系统PATH中

3. 网络连接需要能够访问樱花动漫网站

4. 建议添加适当的请求延迟以避免被封IP