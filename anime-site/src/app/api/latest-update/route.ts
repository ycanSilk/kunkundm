import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import { promises as fs } from 'fs';
import path from 'path';

// 定义响应类型
interface LatestUpdateItem {
  title: string;
  cover_image: string;
  detail_url: string;
  episode_info?: string;
  anime_type?: string;
  current_episode?: number;
}

interface CrawlerResponse {
  success: boolean;
  data: LatestUpdateItem[];
  total_count: number;
  timestamp: string;
  source_url: string;
  error?: string;
}

// 模拟爬虫数据
function getMockLatestUpdates(): LatestUpdateItem[] {
  return [
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
    },
    {
      title: "光死去的夏天",
      cover_image: "http://css.yhdmtu.xyz/news/2023/10/07/20250165.jpg",
      detail_url: "http://www.iyinghua.com/show/6559.html",
      episode_info: "更新至3集",
      current_episode: 3
    },
    {
      title: "魔天记",
      cover_image: "http://css.yhdmtu.xyz/news/2023/10/07/8a1165eec0gy.jpg",
      detail_url: "http://www.iyinghua.com/show/6524.html",
      episode_info: "更新至15集",
      current_episode: 15
    },
    {
      title: "公爵千金的家庭教师",
      cover_image: "http://css.yhdmtu.xyz/news/2023/10/07/20250170.jpg",
      detail_url: "http://www.iyinghua.com/show/6526.html",
      episode_info: "更新至6集",
      current_episode: 6
    }
  ];
}

// 调用Python爬虫获取最新更新
async function getRealLatestUpdates(limit: number = 50): Promise<LatestUpdateItem[]> {
  return new Promise((resolve, reject) => {
    const pythonPath = path.join(process.cwd(), 'src', 'app', 'python', 'crawler_manager.py');
    const pythonExecutable = process.platform === 'win32' ? 'python' : 'python3';
    
    const process = spawn(pythonExecutable, [pythonPath, 'latest', limit.toString()], {
      cwd: path.join(process.cwd(), 'src', 'app', 'python'),
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });

    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    process.on('close', (code) => {
      if (code !== 0) {
        console.error('Python爬虫执行错误:', stderr);
        // 如果爬虫失败，使用模拟数据作为回退
        console.log('使用模拟数据作为回退');
        resolve(getMockLatestUpdates());
        return;
      }

      try {
        // 清理输出，只提取JSON部分
        const lines = stdout.trim().split('\n');
        let jsonStr = '';
        let jsonStarted = false;
        
        for (const line of lines) {
          if (line.trim().startsWith('{') || line.trim().startsWith('[')) {
            jsonStarted = true;
          }
          if (jsonStarted) {
            jsonStr += line;
          }
        }
        
        if (!jsonStr) {
          jsonStr = stdout.trim();
        }

        const result = JSON.parse(jsonStr);
        if (result.success && result.data) {
          // 转换数据格式以匹配接口定义
          const formattedData = result.data.map((item: any) => ({
            title: item.title || '未知标题',
            cover_image: item.cover_image || '',
            detail_url: item.detail_url || '',
            episode_info: item.episode_info || '',
            anime_type: item.anime_type || '',
            current_episode: item.current_episode || 1
          }));
          resolve(formattedData);
        } else {
          console.log('爬虫返回格式错误，使用模拟数据');
          resolve(getMockLatestUpdates());
        }
      } catch (error) {
        console.error('解析爬虫数据失败:', error);
        console.log('使用模拟数据作为回退');
        resolve(getMockLatestUpdates());
      }
    });

    process.on('error', (error) => {
      console.error('启动Python进程失败:', error);
      console.log('使用模拟数据作为回退');
      resolve(getMockLatestUpdates());
    });

    // 设置超时
    setTimeout(() => {
      process.kill();
      console.log('Python爬虫超时，使用模拟数据');
      resolve(getMockLatestUpdates());
    }, 15000);
  });
}

// 保存数据到JSON文件
async function saveLatestUpdatesToFile(data: LatestUpdateItem[]): Promise<string> {
  try {
    const dataDir = path.join(process.cwd(), 'data');
    await fs.mkdir(dataDir, { recursive: true });
    
    const filename = `latest_updates_${new Date().toISOString().split('T')[0]}_${Date.now()}.json`;
    const filepath = path.join(dataDir, filename);
    
    const fileContent = {
      data,
      total_count: data.length,
      timestamp: new Date().toISOString(),
      source_url: 'http://www.iyinghua.com'
    };
    
    await fs.writeFile(filepath, JSON.stringify(fileContent, null, 2), 'utf-8');
    return filepath;
  } catch (error) {
    console.error('保存文件失败:', error);
    throw error;
  }
}

// 获取最新更新
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '20');
    const useRealData = searchParams.get('real') === 'true';
    const saveToFile = searchParams.get('save') === 'true';

    let data: LatestUpdateItem[];
    let filePath: string | null = null;
    
    if (useRealData) {
      try {
        console.log('正在调用Python爬虫获取最新更新...');
        data = await getRealLatestUpdates(limit);
        console.log(`成功获取 ${data.length} 条最新更新数据`);
        
        // 保存到文件
        if (saveToFile) {
          try {
            filePath = await saveLatestUpdatesToFile(data);
            console.log(`数据已保存到: ${filePath}`);
          } catch (saveError) {
            console.error('保存文件失败:', saveError);
          }
        }
      } catch (crawlerError) {
        console.error('Python爬虫调用失败:', crawlerError);
        // 如果爬虫失败，回退到模拟数据
        data = getMockLatestUpdates().slice(0, limit);
      }
    } else {
      // 使用模拟数据
      data = getMockLatestUpdates().slice(0, limit);
    }

    // 应用限制
    const limitedData = data.slice(0, limit);

    const response: CrawlerResponse & { filePath?: string | null } = {
      success: true,
      data: limitedData,
      total_count: limitedData.length,
      timestamp: new Date().toISOString(),
      source_url: 'http://www.iyinghua.com',
      filePath: filePath
    };

    return NextResponse.json(response, {
      headers: {
        'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
        'Access-Control-Allow-Origin': '*',
      },
    });

  } catch (error) {
    console.error('获取最新更新失败:', error);
    
    const errorResponse: CrawlerResponse = {
      success: false,
      data: [],
      total_count: 0,
      timestamp: new Date().toISOString(),
      source_url: 'http://www.iyinghua.com',
      error: error instanceof Error ? error.message : '未知错误'
    };

    return NextResponse.json(errorResponse, { status: 500 });
  }
}

// 支持POST请求（用于触发实时爬取）
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { useRealData = true, limit = 50, saveToFile = true } = body;

    let data: LatestUpdateItem[];
    let filePath: string | null = null;

    if (useRealData) {
      try {
        console.log('正在调用Python爬虫获取最新更新...');
        data = await getRealLatestUpdates(limit);
        console.log(`成功获取 ${data.length} 条最新更新数据`);
        
        // 保存到文件
        if (saveToFile) {
          try {
            filePath = await saveLatestUpdatesToFile(data);
            console.log(`数据已保存到: ${filePath}`);
          } catch (saveError) {
            console.error('保存文件失败:', saveError);
          }
        }
      } catch (crawlerError) {
        console.error('Python爬虫调用失败:', crawlerError);
        // 如果爬虫失败，回退到模拟数据
        data = getMockLatestUpdates().slice(0, limit);
      }
    } else {
      // 使用模拟数据
      data = getMockLatestUpdates().slice(0, limit);
    }

    const response: CrawlerResponse & { filePath?: string | null } = {
      success: true,
      data: data,
      total_count: data.length,
      timestamp: new Date().toISOString(),
      source_url: 'http://www.iyinghua.com',
      filePath: filePath
    };

    return NextResponse.json(response, {
      headers: {
        'Cache-Control': 'no-cache',
        'Access-Control-Allow-Origin': '*',
      },
    });

  } catch (error) {
    console.error('触发爬取失败:', error);
    
    const errorResponse: CrawlerResponse = {
      success: false,
      data: [],
      total_count: 0,
      timestamp: new Date().toISOString(),
      source_url: 'http://www.iyinghua.com',
      error: error instanceof Error ? error.message : '未知错误'
    };

    return NextResponse.json(errorResponse, { status: 500 });
  }
}

// 支持OPTIONS请求（CORS预检）
export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}