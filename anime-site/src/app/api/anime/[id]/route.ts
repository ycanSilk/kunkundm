import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

// 获取特定动漫详情
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id: animeId } = await params;
    
    if (!animeId) {
      return NextResponse.json({
        success: false,
        error: 'Anime ID is required'
      }, { status: 400 });
    }

    // 调用Python爬虫脚本获取真实数据
    const pythonScript = path.join(process.cwd(), 'src', 'app', 'python', 'crawler_episodes.py');
    
    return new Promise((resolve) => {
      const pythonProcess = spawn('python', [pythonScript, animeId], {
        cwd: process.cwd()
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
        if (code === 0) {
          try {
            const result = JSON.parse(output);
            
            if (result.success) {
              // 格式化数据以匹配前端需求
              const formattedData = {
                id: animeId,
                title: result.anime_title,
                titleEn: '',
                episodes: result.total_episodes,
                coverImage: `https://via.placeholder.com/400x600/8B5CF6/FFFFFF?text=${encodeURIComponent(result.anime_title)}`,
                description: `《${result.anime_title}》是一部精彩的动漫作品，共${result.total_episodes}集。`,
                fullDescription: `《${result.anime_title}》是一部精彩的动漫作品，共${result.total_episodes}集。`,
                type: 'TV动画',
                year: 2024,
                season: '春季',
                studio: '未知工作室',
                genres: ['动画', '冒险', '剧情'],
                rating: 8.5,
                duration: '24分钟/集',
                status: '连载中',
                broadcastDay: '周日',
                episodesList: result.data.map((episode: any) => ({
                  id: episode.episode,
                  title: episode.title,
                  duration: '24分钟',
                  airDate: `2024年${Math.floor((episode.episode-1) / 4) + 1}月${((episode.episode-1) % 4) * 7 + 1}日`,
                  thumbnail: `https://via.placeholder.com/300x200/8B5CF6/FFFFFF?text=EP${episode.episode}`,
                  description: `${result.anime_title} 第${episode.episode}集`,
                  url: episode.url
                }))
              };
              
              resolve(NextResponse.json({
                success: true,
                data: formattedData
              }));
            } else {
              resolve(NextResponse.json({
                success: false,
                error: result.error || 'Failed to fetch anime data',
                id: animeId
              }, { status: 404 }));
            }
          } catch (parseError) {
            resolve(NextResponse.json({
              success: false,
              error: 'Failed to parse crawler response',
              details: parseError instanceof Error ? parseError.message : 'Unknown parse error',
              rawOutput: output,
              errorLog: error
            }, { status: 500 }));
          }
        } else {
          resolve(NextResponse.json({
            success: false,
            error: 'Python crawler failed',
            details: error || `Process exited with code ${code}`,
            rawOutput: output
          }, { status: 500 }));
        }
      });

      pythonProcess.on('error', (err) => {
        resolve(NextResponse.json({
          success: false,
          error: 'Failed to spawn Python process',
          details: err.message
        }, { status: 500 }));
      });
    });

  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to fetch anime details',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}