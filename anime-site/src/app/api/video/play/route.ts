import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

interface PlayRequest {
  url: string;
  title?: string;
  episode?: string;
  totalEpisodes?: string;
  cover?: string;
}

interface PlayResponse {
  success: boolean;
  data: {
    videoUrl: string;
    title?: string;
    episode?: string;
    totalEpisodes?: string;
    cover?: string;
    sourceUrl: string;
  };
  error?: string;
}

export async function GET(request: NextRequest): Promise<NextResponse> {
  const searchParams = request.nextUrl.searchParams;
  const url = searchParams.get('url');
  const title = searchParams.get('title');
  const episode = searchParams.get('episode');
  const totalEpisodes = searchParams.get('totalEpisodes');
  const cover = searchParams.get('cover');

  if (!url) {
    return NextResponse.json<PlayResponse>(
      { success: false, error: '缺少URL参数', data: { videoUrl: '', sourceUrl: '' } },
      { status: 400 }
    );
  }

  try {
    // 调用Python爬虫脚本
    const pythonScript = path.join(process.cwd(), 'src', 'app', 'python', 'crawler_video.py');
    
    const result = await new Promise<string>((resolve, reject) => {
      const pythonProcess = spawn('python', [pythonScript, url], {
        stdio: ['pipe', 'pipe', 'pipe'],
        env: {
          ...process.env,
          PYTHONIOENCODING: 'utf-8'
        }
      });

      let output = '';
      let error = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        error += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(error || 'Python脚本执行失败'));
        } else {
          resolve(output.trim());
        }
      });

      pythonProcess.on('error', (err) => {
        reject(err);
      });
    });

    // 解析Python脚本的输出
    const data = JSON.parse(result);
    
    // 从URL中提取集数信息
    const episodeMatch = url.match(/\/v\/(\d+)-(\d+)\.html/);
    let episodeNum = episodeMatch ? parseInt(episodeMatch[2]) : 1;
    
    // 格式化为两位数，如01, 02, 12等
    const formattedEpisode = episodeNum.toString().padStart(2, '0');
    
    // 拼接最终的视频URL
    const videoUrl = `https://tup.iyinghua.com/?vid=${data.url}/第${formattedEpisode}集/index.m3u8$mp4`;
    
    return NextResponse.json<PlayResponse>({
      success: true,
      data: {
        videoUrl: videoUrl,
        title: title || undefined,
        episode: episode || formattedEpisode,
        totalEpisodes: totalEpisodes || undefined,
        cover: cover || undefined,
        sourceUrl: url
      }
    });

  } catch (error) {
    console.error('API错误:', error);
    return NextResponse.json<PlayResponse>(
      { 
        success: false,
        error: error instanceof Error ? error.message : '获取视频URL失败',
        data: { videoUrl: '', sourceUrl: url }
      },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body: PlayRequest = await request.json();
    const { url, title, episode, totalEpisodes, cover } = body;
    
    if (!url) {
      return NextResponse.json<PlayResponse>(
        { success: false, error: '缺少URL参数', data: { videoUrl: '', sourceUrl: '' } },
        { status: 400 }
      );
    }

    // 重用GET逻辑
    const searchParams = new URLSearchParams();
    searchParams.set('url', url);
    if (title) searchParams.set('title', title);
    if (episode) searchParams.set('episode', episode);
    if (totalEpisodes) searchParams.set('totalEpisodes', totalEpisodes);
    if (cover) searchParams.set('cover', cover);
    
    const getRequest = new NextRequest(
      new URL(`/api/video/play?${searchParams.toString()}`, request.url)
    );
    
    return GET(getRequest);
  } catch (error) {
    return NextResponse.json<PlayResponse>(
      { 
        success: false,
        error: '请求格式错误',
        data: { videoUrl: '', sourceUrl: '' }
      },
      { status: 400 }
    );
  }
}