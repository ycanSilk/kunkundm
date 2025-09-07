// 基础类型定义
export interface CrawlerConfig {
  id: string;
  name: string;
  description: string;
  baseUrl: string;
  endpoints: {
    [key: string]: EndpointConfig;
  };
  selectors: {
    [key: string]: string;
  };
  parameters: {
    [key: string]: ParameterConfig;
  };
  headers: Record<string, string>;
  rateLimit: RateLimitConfig;
}

interface EndpointConfig {
  path: string;
  method: 'GET' | 'POST';
  description: string;
  requiredParams: string[];
  optionalParams?: string[];
  responseFormat: 'json' | 'html';
}

interface ParameterConfig {
  type: 'path' | 'query' | 'body';
  required: boolean;
  description: string;
  validation?: RegExp;
  defaultValue?: string | number;
}

interface RateLimitConfig {
  requests: number;
  interval: number; // milliseconds
  burst?: number;
}

// 基础配置
export const API_CONFIG = {
  BASE_URL: process.env.NODE_ENV === 'production' 
    ? 'https://anime-site-api.example.com' 
    : 'http://localhost:3000',
  
  API_ENDPOINTS: {
    anime: '/api/anime',
    crawler: '/api/crawler',
    recommendations: '/api/recommendations'
  },

  PAGINATION: {
    DEFAULT_PAGE: 1,
    DEFAULT_LIMIT: 20,
    MAX_LIMIT: 100
  }
};

// 4个独立爬虫配置
export const crawlerConfigs = {
  // 1. 完整动漫列表爬虫
  complete_list: {
    id: 'complete_list',
    name: '樱花动漫完整列表爬虫',
    description: '爬取樱花动漫所有分类(A-Z+其他)的完整动漫数据',
    baseUrl: 'http://m.iyinghua.com',
    endpoints: {
      all_anime: {
        path: '/all/',
        method: 'GET' as const,
        description: '获取所有动漫列表',
        requiredParams: [],
        optionalParams: ['page', 'category'],
        responseFormat: 'html' as const
      }
    },
    selectors: {
      // 分类识别
      categoryContainer: 'div.mlist',
      categoryName: 'div.mlist h2',
      
      // 动漫信息
      animeItem: 'div.mlist li',
      animeTitle: 'div.mlist li a',
      animeDetailUrl: 'div.mlist li a[href]',
      
      // 集数信息
      episodeCount: 'div.mlist li em',
      episodeUrl: 'div.mlist li a[href]'
    },
    parameters: {
      page: {
        type: 'query' as const,
        required: false,
        description: '页码',
        defaultValue: 1,
        validation: /^\d+$/
      }
    },
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Referer': 'http://m.iyinghua.com'
    },
    rateLimit: {
      requests: 3,
      interval: 2000
    }
  },

  // 2. 搜索爬虫
  search: {
    id: 'search',
    name: '樱花动漫搜索爬虫',
    description: '通过关键词搜索动漫，获取搜索结果列表',
    baseUrl: 'http://www.iyinghua.com',
    endpoints: {
      search: {
        path: '/search/{keyword}/',
        method: 'GET' as const,
        description: '搜索动漫',
        requiredParams: ['keyword'],
        optionalParams: ['page'],
        responseFormat: 'html' as const
      }
    },
    selectors: {
      // 搜索结果
      searchResult: 'div.lpic li',
      
      // 图片信息
      coverImage: 'div.lpic li img',
      coverAlt: 'div.lpic li img[alt]',
      
      // 动漫详情
      animeTitle: 'div.lpic li h2 a',
      animeDetailUrl: 'div.lpic li h2 a[href]',
      
      // 集数信息
      episodeInfo: 'div.lpic li span',
      
      // 类型识别
      animeType: 'div.lpic li span:contains("类型：")',
      description: 'div.lpic li p'
    },
    parameters: {
      keyword: {
        type: 'path' as const,
        required: true,
        description: '搜索关键词',
        validation: /^[a-zA-Z0-9\u4e00-\u9fa5]+$/
      },
      page: {
        type: 'query' as const,
        required: false,
        description: '页码',
        defaultValue: 1,
        validation: /^\d+$/
      }
    },
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Referer': 'http://www.iyinghua.com'
    },
    rateLimit: {
      requests: 2,
      interval: 3000
    }
  },

  // 3. 视频URL解析器
  video_parser: {
    id: 'video_parser',
    name: '樱花动漫视频URL解析器',
    description: '解析樱花动漫页面URL为真实视频播放地址',
    baseUrl: 'http://www.iyinghua.com',
    endpoints: {
      parse_video: {
        path: '/{play_path}',
        method: 'GET' as const,
        description: '解析真实视频地址',
        requiredParams: ['play_path'],
        responseFormat: 'html' as const
      }
    },
    selectors: {
      // 视频URL提取
      videoUrl: '',
      // 正则表达式匹配
      m3u8Pattern: 'https?:\\/\\/.*\\.m3u8',
      tupPattern: 'tup[^\'"]*\\.mp4',
      vidPattern: 'vid=([^&]+)',
      
      // 页面信息
      pageTitle: 'title',
      currentEpisode: '.play .num',
      totalEpisodes: '.play .total'
    },
    parameters: {
      play_path: {
        type: 'path' as const,
        required: true,
        description: '播放页面路径',
        validation: /^[\w\-\/]+\.html$/
      }
    },
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Referer': 'http://www.iyinghua.com'
    },
    rateLimit: {
      requests: 1,
      interval: 1000
    }
  },

  // 4. 分集URL爬虫
  episode_crawler: {
    id: 'episode_crawler',
    name: '樱花动漫分集URL爬虫',
    description: '爬取动漫详情页的所有分集播放URL',
    baseUrl: 'http://www.iyinghua.com',
    endpoints: {
      get_episodes: {
        path: '/show/{id}.html',
        method: 'GET' as const,
        description: '获取分集列表',
        requiredParams: ['id'],
        responseFormat: 'html' as const
      }
    },
    selectors: {
      // 动漫信息
      animeTitle: 'h1',
      
      // 分集列表
      episodeContainer: 'div.movurl',
      episodeList: 'div.movurl li',
      
      // 分集信息
      episodeNumber: 'div.movurl li a',
      episodeTitle: 'div.movurl li a',
      episodeUrl: 'div.movurl li a[href]'
    },
    parameters: {
      id: {
        type: 'path' as const,
        required: true,
        description: '动漫ID',
        validation: /^\d+$/
      }
    },
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Referer': 'http://www.iyinghua.com'
    },
    rateLimit: {
      requests: 2,
      interval: 2000
    }
  },

  // 5. 最新更新爬虫
  latest_update: {
    id: 'latest_update',
    name: '樱花动漫最新更新爬虫',
    description: '爬取樱花动漫首页的最新更新动漫列表',
    baseUrl: 'http://www.iyinghua.com',
    endpoints: {
      home: {
        path: '/',
        method: 'GET' as const,
        description: '获取首页最新更新',
        requiredParams: [],
        responseFormat: 'html' as const
      }
    },
    selectors: {
      // 容器
      container: '.area .img ul li',
      
      // 图片信息
      coverImage: 'img[src]',
      coverAlt: 'img[alt]',
      
      // 动漫详情
      title: 'a[title]',
      detailUrl: 'a[href]',
      
      // 更新信息
      episodeInfo: 'span',
      animeType: 'span',
      description: 'p'
    },
    parameters: {},
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Referer': 'http://www.iyinghua.com',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1'
    },
    rateLimit: {
      requests: 1,
      interval: 1000
    }
  }
};

// 使用工具函数
export const getCrawlerConfig = (crawlerId: string) => {
  return crawlerConfigs[crawlerId as keyof typeof crawlerConfigs];
};

export const buildUrl = (crawlerId: string, endpoint: string, params: Record<string, string | number>) => {
  const config = getCrawlerConfig(crawlerId);
  const endpointConfig = config.endpoints[endpoint];
  
  let url = `${config.baseUrl}${endpointConfig.path}`;
  
  // 替换路径参数
  Object.keys(params).forEach(key => {
    url = url.replace(`{${key}}`, String(params[key]));
  });
  
  return url;
};

export const getSelectors = (crawlerId: string) => {
  return getCrawlerConfig(crawlerId).selectors;
};

export const getHeaders = (crawlerId: string) => {
  return getCrawlerConfig(crawlerId).headers;
};

export const getRateLimit = (crawlerId: string) => {
  return getCrawlerConfig(crawlerId).rateLimit;
};

// 导出所有爬虫ID
export const CRAWLER_IDS = Object.keys(crawlerConfigs) as Array<keyof typeof crawlerConfigs>;

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  timestamp: number;
}

export interface PaginationParams {
  page?: number;
  limit?: number;
  sort?: string;
  order?: 'asc' | 'desc';
}