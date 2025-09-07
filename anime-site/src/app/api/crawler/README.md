# 爬虫API文档

## 最新更新API

### GET /api/crawler/latest-update
获取樱花动漫首页最新更新内容。

#### 请求参数
- `limit` (可选): 返回结果数量限制，默认20
- `real` (可选): 是否使用真实数据，默认false（使用模拟数据）

#### 响应格式
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
  "total_count": 40,
  "timestamp": "2024-01-15T10:30:00.000Z",
  "source_url": "http://www.iyinghua.com"
}
```

#### 使用示例
```typescript
// 使用Hook
import { useLatestUpdates } from '@/lib/hooks/useCrawler';

function LatestUpdatesComponent() {
  const { data, loading, error } = useLatestUpdates(10, true);
  
  if (loading) return <div>加载中...</div>;
  if (error) return <div>错误: {error}</div>;
  
  return (
    <div>
      {data.map(item => (
        <div key={item.detail_url}>
          <img src={item.cover_image} alt={item.title} />
          <h3>{item.title}</h3>
          <p>{item.episode_info}</p>
        </div>
      ))}
    </div>
  );
}

// 直接调用API
const response = await fetch('/api/crawler/latest-update?limit=10&real=true');
const data = await response.json();
```

### POST /api/crawler/latest-update
手动触发最新更新爬取。

#### 请求体
```json
{
  "useRealData": true
}
```

## 测试API

### GET /api/crawler/test
获取所有可用的爬虫API端点信息。

## 配置更新

最新更新爬虫配置已添加到 `src/config/api.config.ts`：

```typescript
latest_update: {
  id: 'latest_update',
  name: '樱花动漫最新更新爬虫',
  description: '爬取樱花动漫首页的最新更新动漫列表',
  baseUrl: 'http://www.iyinghua.com',
  selectors: {
    container: '.area .img ul li',
    coverImage: 'img[src]',
    title: 'a[title]',
    detailUrl: 'a[href]',
    episodeInfo: 'span',
    animeType: 'span'
  }
}
```

## Python集成

要启用真实数据爬取，需要：

1. 安装Python依赖：
```bash
cd 最新更新
pip install -r requirements.txt
```

2. 运行Python集成服务：
```bash
python src/scripts/run-crawler.py latest_update
```

3. 修改 `src/lib/crawler-service.ts` 中的服务调用逻辑