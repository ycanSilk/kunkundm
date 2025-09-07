import { NextRequest, NextResponse } from 'next/server';

// 导入数据存储
import { crawlerStore } from '@/lib/crawler-store';

// 获取所有动漫列表
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action');
  
  try {
    switch (action) {
      case 'list':
        return NextResponse.json({
          success: true,
          data: crawlerStore.getAnimeList(),
          count: crawlerStore.getAnimeList().length,
          lastUpdated: crawlerStore.getLastUpdated()
        });
        
      case 'weekly':
        return NextResponse.json({
          success: true,
          data: crawlerStore.getWeeklyUpdates()
        });
        
      case 'search':
        const query = searchParams.get('q') || '';
        const results = crawlerStore.getSearchResults(query);
        return NextResponse.json({
          success: true,
          data: results,
          query,
          count: results.length
        });
        
      default:
        return NextResponse.json({
          success: true,
          message: 'Anime API is running',
          endpoints: {
            '/api/anime?action=list': 'Get all anime list',
            '/api/anime?action=weekly': 'Get weekly updates',
            '/api/anime?action=search&q=keyword': 'Search anime'
          }
        });
    }
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to fetch anime data',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

// 接收Python爬虫数据
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { type, data, source } = body;
    
    if (!type || !data) {
      return NextResponse.json({
        success: false,
        error: 'Missing required fields: type and data'
      }, { status: 400 });
    }
    
    // 接收爬虫数据（已废弃，请使用 /api/crawler 端点）
      case 'crawler':
        return NextResponse.json({
          success: false,
          error: 'This endpoint is deprecated. Please use /api/crawler instead',
          redirect: '/api/crawler'
        }, { status: 410 });
        
      default:
        return NextResponse.json({
          success: false,
          error: 'Invalid type provided'
        }, { status: 400 });
    }
    
    return NextResponse.json({
      success: true,
      message: `Successfully updated ${type}`,
      count: Array.isArray(data) ? data.length : Object.keys(data).length,
      source: source || 'unknown'
    });
    
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to process request',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}