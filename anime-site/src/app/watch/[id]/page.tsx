'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useParams } from 'next/navigation';
import dynamic from 'next/dynamic';
import { Play } from 'lucide-react';

// 动态导入ArtPlayer组件，避免SSR问题
const ArtPlayer = dynamic(() => import('@/components/ArtPlayer'), {
  ssr: false,
  loading: () => (
    <div className="w-full aspect-video bg-gray-800 rounded-lg flex items-center justify-center">
      <div className="text-gray-400">加载播放器中...</div>
    </div>
  ),
});

import { Header } from '@/components/header';
import { Footer } from '@/components/footer';

// 移除mock数据，使用真实视频URL

const mockEpisodes = Array.from({ length: 28 }, (_, i) => ({
  id: i + 1,
  title: `第${i + 1}集`,
  thumbnail: `${i + 1}`,
  videoUrl: ``
}));

export default function WatchPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  
  // 移除播放源状态，使用真实视频URL
  const [currentEpisode, setCurrentEpisode] = useState(1);
  const [currentVideoUrl, setCurrentVideoUrl] = useState('');
  const [loading, setLoading] = useState(true);
  const [animeData, setAnimeData] = useState<any>(null);
  const [pageTitle, setPageTitle] = useState('');
  const [pageCover, setPageCover] = useState('');
  const [totalEpisodes, setTotalEpisodes] = useState(0);
  const [episodes, setEpisodes] = useState<any[]>([]);

  useEffect(() => {
    const episodeParam = searchParams?.get('episode');
    const urlParam = searchParams?.get('url');
    const titleParam = searchParams?.get('title');
    const coverParam = searchParams?.get('cover');
    const totalEpisodesParam = searchParams?.get('totalEpisodes');
    const animeId = params?.id as string;
    
    console.group('🎯 Watch页面参数调试');
    console.log('📥 输入参数:');
    console.log('  - animeId:', animeId);
    console.log('  - episode:', episodeParam);
    console.log('  - url:', urlParam);
    console.log('  - title:', titleParam);
    console.log('  - cover:', coverParam);
    console.log('  - totalEpisodes:', totalEpisodesParam);
    console.log('  - 完整URL:', window.location.href);
    console.groupEnd();
    
    if (episodeParam) {
      const episodeNum = parseInt(episodeParam, 10);
      setCurrentEpisode(episodeNum);
    }
    
    // 使用传递过来的参数
    if (urlParam) {
      setCurrentVideoUrl(decodeURIComponent(urlParam));
    }
    if (titleParam) {
      setPageTitle(decodeURIComponent(titleParam));
    }
    if (coverParam) {
      setPageCover(decodeURIComponent(coverParam));
    }
    if (totalEpisodesParam) {
      setTotalEpisodes(parseInt(totalEpisodesParam, 10));
    }
    
    // 获取动漫详情和集数列表
    if (animeId) {
      const apiUrl = `/api/anime/${animeId}`;
      console.group('🔍 爬虫脚本执行调试');
      console.log('🚀 开始获取动漫详情...');
      console.log('📡 API请求地址:', apiUrl);
      console.log('⏰ 请求时间:', new Date().toLocaleString());
      
      fetch(apiUrl)
        .then(res => {
          console.log('📤 响应状态:', res.status, res.statusText);
          console.log('📋 响应头:', Object.fromEntries(res.headers.entries()));
          return res.json();
        })
        .then(data => {
          console.group('🕷️ 爬虫脚本执行结果');
          console.log('📦 爬虫返回原始数据:', data);
          
          if (data.success && data.data) {
            console.log('✅ 爬虫执行成功');
            console.log('📊 数据概览:', {
              title: data.data.title,
              totalEpisodes: data.data.episodesList?.length || 0,
              hasCover: !!data.data.cover,
              hasDescription: !!data.data.description,
              sourceUrl: data.data.sourceUrl
            });
            
            setAnimeData(data.data);
            setEpisodes(data.data.episodesList || []);
            
            console.log('📋 集数详情:');
            if (data.data.episodesList) {
              data.data.episodesList.forEach((ep: any, index: number) => {
                console.log(`  第${index + 1}集:`, {
                  id: ep.id,
                  title: ep.title,
                  url: ep.videoUrl,
                  isCurrent: ep.id === (parseInt(episodeParam || '1'))
                });
              });
            }
            
            console.log('📊 统计信息:', {
              totalEpisodes: data.data.episodesList?.length || 0,
              episodesArray: data.data.episodesList
            });
            
            // 设置默认集数
            if (data.data.episodesList && data.data.episodesList.length > 0) {
              const episodeNum = parseInt(episodeParam || '1', 10);
              const validEpisode = Math.min(Math.max(1, episodeNum), data.data.episodesList.length);
              setCurrentEpisode(validEpisode);
            }
          } else {
            console.error('❌ 爬虫执行失败:', data.error);
            console.log('📋 错误详情:', data);
          }
          console.groupEnd();
        })
        .catch(error => {
          console.group('❗ 爬虫执行异常');
          console.error('❌ 获取动漫详情失败:', error);
          console.log('📝 错误类型:', error.name);
          console.log('📝 错误消息:', error.message);
          console.log('📝 错误堆栈:', error.stack);
          console.groupEnd();
        });
    }
  }, [searchParams, params?.id]);

  useEffect(() => {
    const videoId = params?.id as string;
    const urlParam = searchParams?.get('url');
    
    console.group('🎬 视频URL解析调试');
    console.log('📥 输入参数:');
    console.log('  - videoId:', videoId);
    console.log('  - urlParam:', urlParam);
    console.log('  - episodes:', episodes);
    console.log('  - currentEpisode:', currentEpisode);
    
    if (videoId && urlParam) {
      setLoading(true);
      const decodedUrl = decodeURIComponent(urlParam);
      console.log('🔗 解码后的URL:', decodedUrl);
      
      // 使用新的视频解析API获取真实的视频URL
      const apiUrl = `/api/video/play?url=${encodeURIComponent(decodedUrl)}`;
      console.log('📡 请求视频解析API:', apiUrl);
      
      fetch(apiUrl)
        .then(res => res.json())
        .then(data => {
          console.group('🔍 视频解析结果');
          console.log('✅ 视频解析API返回:', data);
          
          if (data.success && data.data?.video_url) {
            console.log('🎯 解析成功 - 真实视频URL:', data.data.video_url);
            console.log('📊 解析详情:', {
              title: data.data.title,
              current_episode: data.data.current_episode,
              total_episodes: data.data.total_episodes,
              source_url: data.data.source_url,
              parsed_at: data.data.parsed_at
            });
            setCurrentVideoUrl(data.data.video_url);
          } else {
            console.warn('⚠️ 视频解析失败，使用原始URL:', decodedUrl);
            console.log('❌ 错误详情:', data.error || data);
            setCurrentVideoUrl(decodedUrl);
          }
          console.groupEnd();
        })
        .catch(error => {
          console.error('❌ API调用失败:', error);
          console.log('🔙 回退到原始URL:', decodedUrl);
          setCurrentVideoUrl(decodedUrl);
        })
        .finally(() => {
          setLoading(false);
          console.groupEnd();
        });
    } else if (episodes.length > 0 && currentEpisode <= episodes.length) {
      // 如果有真实的集数数据，使用当前集的URL
      const currentEpisodeData = episodes.find(ep => ep.id === currentEpisode);
      console.log('📺 使用真实集数数据:', {
        currentEpisodeData,
        episodeUrl: currentEpisodeData?.videoUrl
      });
      
      if (currentEpisodeData && currentEpisodeData.videoUrl) {
        setLoading(true);
        console.log('🔗 解析集数URL:', currentEpisodeData.videoUrl);
        
        fetch(`/api/video/play?url=${encodeURIComponent(currentEpisodeData.videoUrl)}`)
          .then(res => res.json())
          .then(data => {
            console.group('🔍 集数视频解析结果');
            console.log('✅ 集数解析成功:', data);
            
            if (data.success && data.data?.video_url) {
              console.log('🎯 集数真实视频URL:', data.data.video_url);
              setCurrentVideoUrl(data.data.video_url);
            } else {
              console.log('⚠️ 集数解析失败，使用原始URL:', currentEpisodeData.videoUrl);
              setCurrentVideoUrl(currentEpisodeData.videoUrl);
            }
            console.groupEnd();
          })
          .catch(() => {
            console.log('❌ 集数解析API失败，使用原始URL:', currentEpisodeData.videoUrl);
            setCurrentVideoUrl(currentEpisodeData.videoUrl);
          })
          .finally(() => {
            setLoading(false);
          });
      }
    } else {
      console.log('📝 无有效URL参数，等待数据加载...');
      setLoading(false);
    }
    console.groupEnd();
  }, [params?.id, searchParams, episodes, currentEpisode]);

  // 移除这个useEffect，因为它会覆盖真实URL为mock数据
  // useEffect(() => {
  //   const source = mockVideoSources[currentSource];
  //   setCurrentVideoUrl(source.url);
  // }, [currentSource]);

  // 移除播放源切换功能，使用真实视频URL

  const handleEpisodeChange = (episode: number) => {
    console.group('🔄 切换集数调试');
    console.log('📋 切换前状态:', {
      currentEpisode,
      targetEpisode: episode,
      episodesCount: episodes.length
    });
    
    setCurrentEpisode(episode);
    
    // 获取当前集数的URL
    const currentEpisodeData = episodes.find(ep => ep.id === episode);
    console.log('🎯 目标集数数据:', currentEpisodeData);
    
    if (currentEpisodeData && currentEpisodeData.videoUrl) {
      console.log('🔗 开始解析集数URL:', currentEpisodeData.videoUrl);
      setLoading(true);
      
      const apiUrl = `/api/video/play?url=${encodeURIComponent(currentEpisodeData.videoUrl)}`;
      console.log('📡 请求API:', apiUrl);
      
      fetch(apiUrl)
        .then(res => res.json())
        .then(data => {
          console.group('🔍 集数切换解析结果');
          console.log('✅ 解析返回:', data);
          
          if (data.success && data.data?.video_url) {
            console.log('🎯 解析成功 - 新视频URL:', data.data.video_url);
            setCurrentVideoUrl(data.data.video_url);
          } else {
            console.warn('⚠️ 解析失败，使用原始URL:', currentEpisodeData.videoUrl);
            console.log('❌ 错误详情:', data.error || data);
            setCurrentVideoUrl(currentEpisodeData.videoUrl);
          }
          console.groupEnd();
        })
        .catch(error => {
          console.error('❌ 集数解析API调用失败:', error);
          console.log('🔙 回退到原始URL:', currentEpisodeData.videoUrl);
          setCurrentVideoUrl(currentEpisodeData.videoUrl);
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      console.log('⚠️ 未找到目标集数数据或URL为空');
    }
    
    // 更新URL参数，保持当前页面状态
    const newUrl = new URL(window.location.href);
    newUrl.searchParams.set('episode', episode.toString());
    window.history.pushState({}, '', newUrl.toString());
    console.log('🌐 更新页面URL:', newUrl.toString());
    console.groupEnd();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
              <p className="mt-4 text-lg text-gray-300">加载中...</p>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* 播放器区域 */}
        <div className="mb-4">
          <div className="bg-black rounded-lg overflow-hidden aspect-video max-w-4xl mx-auto">
            <ArtPlayer
              url={currentVideoUrl}
              title={`${pageTitle || animeData?.title || ''} 第${currentEpisode}集`}
              className="rounded-lg"
              onPrev={() => handleEpisodeChange(Math.max(1, currentEpisode - 1))}
              onNext={() => handleEpisodeChange(Math.min(totalEpisodes || episodes.length, currentEpisode + 1))}
              hasPrev={currentEpisode > 1}
              hasNext={currentEpisode < (totalEpisodes || episodes.length)}
            />
          </div>
        </div>



        {/* 集数列表 */}
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="text-white text-lg font-semibold mb-3">
              剧集列表 ({totalEpisodes || episodes.length}集)
              <span className="text-sm text-gray-400 ml-2">当前第 {currentEpisode} 集</span>
            </h3>
          <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10 xl:grid-cols-12 gap-2">
            {episodes.map((episode) => (
              <button
                key={episode.id}
                onClick={() => handleEpisodeChange(episode.id)}
                className={`cursor-pointer rounded transition-all duration-200 text-center py-2 px-1 text-xs font-medium ${
                  currentEpisode === episode.id
                    ? 'bg-purple-600 text-white ring-2 ring-purple-500'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                第{episode.id}集
              </button>
            ))}
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}