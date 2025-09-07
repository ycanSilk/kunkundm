import { NextRequest, NextResponse } from 'next/server';

// 测试所有爬虫API
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type') || 'all';

    const results = {
      timestamp: new Date().toISOString(),
      endpoints: {
        latest_update: {
          url: '/api/latest-update',
          method: 'GET',
          params: ['limit', 'real'],
          description: '获取樱花动漫最新更新'
        },
        search: {
          url: '/api/crawler/search',
          method: 'GET',
          params: ['query'],
          description: '搜索动漫'
        },
        complete_list: {
          url: '/api/crawler/complete-list',
          method: 'GET',
          params: ['page'],
          description: '获取完整动漫列表'
        },
        episodes: {
          url: '/api/crawler/episodes',
          method: 'GET',
          params: ['id'],
          description: '获取动漫分集列表'
        },
        video_parser: {
          url: '/api/crawler/video-parser',
          method: 'GET',
          params: ['id', 'episode'],
          description: '解析视频播放地址'
        }
      }
    };

    return NextResponse.json(results);

  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : '未知错误' },
      { status: 500 }
    );
  }
}