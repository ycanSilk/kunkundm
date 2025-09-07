import { useState, useEffect } from 'react';

// 爬虫数据类型
export interface CrawlerData {
  title: string;
  cover_image: string;
  detail_url: string;
  episode_info?: string;
  anime_type?: string;
  current_episode?: number;
}

export interface CrawlerResponse {
  success: boolean;
  data: CrawlerData[];
  total_count: number;
  timestamp: string;
  source_url: string;
  error?: string;
}

// 爬虫Hook
export function useLatestUpdates(limit: number = 20, realData: boolean = false) {
  const [data, setData] = useState<CrawlerData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLatestUpdates = async () => {
      try {
        setLoading(true);
        setError(null);

        const params = new URLSearchParams();
        if (limit !== 20) params.append('limit', limit.toString());
        if (realData) params.append('real', 'true');

        const response = await fetch(`/api/latest-update?${params}`);
        const result: CrawlerResponse = await response.json();

        if (result.success) {
          setData(result.data);
        } else {
          setError(result.error || '获取数据失败');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : '网络错误');
      } finally {
        setLoading(false);
      }
    };

    fetchLatestUpdates();
  }, [limit, realData]);

  return { data, loading, error };
}

// 手动触发爬取
export async function triggerCrawler(type: string, params?: any): Promise<CrawlerResponse> {
  try {
    const response = await fetch(`/api/crawler/${type}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params || {}),
    });

    const result: CrawlerResponse = await response.json();
    return result;
  } catch (error) {
    return {
      success: false,
      data: [],
      total_count: 0,
      timestamp: new Date().toISOString(),
      source_url: '',
      error: error instanceof Error ? error.message : '网络错误'
    };
  }
}

// 测试所有爬虫
export async function testCrawlers() {
  try {
    const response = await fetch('/api/crawler/test');
    return await response.json();
  } catch (error) {
    return { error: error instanceof Error ? error.message : '测试失败' };
  }
}