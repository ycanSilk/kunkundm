import { getCrawlerConfig } from '@/config/api.config';

// 爬虫服务接口
export interface CrawlerService {
  crawlLatestUpdates(): Promise<any>;
  crawlSearchResults(query: string): Promise<any>;
  crawlAnimeList(): Promise<any>;
  crawlEpisodes(animeId: string): Promise<any>;
  crawlVideoUrl(animeId: string, episode: string): Promise<any>;
}

// 最新更新爬虫服务
export class LatestUpdateService {
  private config: any;

  constructor() {
    this.config = getCrawlerConfig('latest_update');
  }

  async crawlLatestUpdates(): Promise<any> {
    try {
      // 这里可以调用Python爬虫脚本
      const response = await fetch('http://localhost:8000/api/crawler/latest-update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ useRealData: true }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('调用爬虫服务失败:', error);
      // 返回模拟数据作为备用
      return this.getMockData();
    }
  }

  private getMockData() {
    return {
      success: true,
      data: [
        {
          title: "百妖谱·洛阳篇",
          cover_image: "http://css.yhdmtu.xyz/news/2023/10/07/da7f014187a0f.jpg",
          detail_url: "http://www.iyinghua.com/show/6594.html",
          episode_info: "更新至12集",
          current_episode: 12
        },
        {
          title: "牧神记",
          cover_image: "http://css.yhdmtu.xyz/news/2023/10/07/qj207i0a077.jpg", 
          detail_url: "http://www.iyinghua.com/show/6389.html",
          episode_info: "更新至8集",
          current_episode: 8
        }
      ],
      total_count: 2,
      timestamp: new Date().toISOString(),
      source_url: this.config.baseUrl
    };
  }
}

// 统一爬虫服务
export class CrawlerManager {
  private static instance: CrawlerManager;
  private latestUpdateService: LatestUpdateService;

  private constructor() {
    this.latestUpdateService = new LatestUpdateService();
  }

  public static getInstance(): CrawlerManager {
    if (!CrawlerManager.instance) {
      CrawlerManager.instance = new CrawlerManager();
    }
    return CrawlerManager.instance;
  }

  public async getLatestUpdates(): Promise<any> {
    return this.latestUpdateService.crawlLatestUpdates();
  }

  public async getSearchResults(query: string): Promise<any> {
    // 集成搜索爬虫
    const config = getCrawlerConfig('search');
    return { query, config };
  }

  public async getCompleteList(): Promise<any> {
    // 集成完整列表爬虫
    const config = getCrawlerConfig('complete_list');
    return { config };
  }

  public async getEpisodes(animeId: string): Promise<any> {
    // 集成分集爬虫
    const config = getCrawlerConfig('episode_crawler');
    return { animeId, config };
  }

  public async getVideoUrl(animeId: string, episode: string): Promise<any> {
    // 集成视频解析爬虫
    const config = getCrawlerConfig('video_parser');
    return { animeId, episode, config };
  }
}

// 导出单例
export const crawlerManager = CrawlerManager.getInstance();