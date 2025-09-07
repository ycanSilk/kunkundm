'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useParams } from 'next/navigation';
import dynamic from 'next/dynamic';
import { Play, Monitor, Server } from 'lucide-react';

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

// 模拟数据 - 包含真实的测试视频URL
const mockVideoSources = [
  { id: 0, name: '高清线路', quality: '1080P', url: 'https://www.w3schools.com/html/mov_bbb.mp4' },
  { id: 1, name: '标清线路', quality: '720P', url: 'https://www.w3schools.com/html/mov_bbb.mp4' },
  { id: 2, name: '备用线路', quality: '480P', url: 'https://www.w3schools.com/html/mov_bbb.mp4' },
];

const mockEpisodes = Array.from({ length: 28 }, (_, i) => ({
  id: i + 1,
  title: `第${i + 1}集`,
  thumbnail: `https://via.placeholder.com/300x200/8B5CF6/FFFFFF?text=EP${i + 1}`,
  videoUrl: `https://www.w3schools.com/html/mov_bbb.mp4`
}));

export default function WatchPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  
  const [currentSource, setCurrentSource] = useState(0);
  const [currentEpisode, setCurrentEpisode] = useState(1);
  const [currentVideoUrl, setCurrentVideoUrl] = useState(mockVideoSources[0].url);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const episodeParam = searchParams?.get('episode');
    if (episodeParam) {
      const episodeNum = parseInt(episodeParam, 10);
      if (episodeNum > 0 && episodeNum <= mockEpisodes.length) {
        setCurrentEpisode(episodeNum);
      }
    }
  }, [searchParams]);

  useEffect(() => {
    const videoId = params?.id as string;
    if (videoId) {
      setLoading(true);
      setTimeout(() => setLoading(false), 1000);
    }
  }, [params?.id, currentEpisode]);

  useEffect(() => {
    const source = mockVideoSources[currentSource];
    setCurrentVideoUrl(source.url);
  }, [currentSource]);

  const handleSourceChange = (index: number) => {
    setCurrentSource(index);
  };

  const handleEpisodeChange = (episode: number) => {
    setCurrentEpisode(episode);
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
              title={`第${currentEpisode}集`}
              className="rounded-lg"
              onPrev={() => handleEpisodeChange(Math.max(1, currentEpisode - 1))}
              onNext={() => handleEpisodeChange(Math.min(mockEpisodes.length, currentEpisode + 1))}
              hasPrev={currentEpisode > 1}
              hasNext={currentEpisode < mockEpisodes.length}
            />
          </div>
        </div>

        {/* 播放源列表 */}
        <div className="bg-gray-800 rounded-lg p-4 mb-4">
          <h3 className="text-white text-lg font-semibold mb-3 flex items-center">
            <Server className="h-5 w-5 mr-2" />
            播放源
          </h3>
          <div className="flex flex-wrap gap-2">
            {mockVideoSources.map((source) => (
              <button
                key={source.id}
                onClick={() => handleSourceChange(source.id)}
                className={`px-3 py-2 rounded text-sm font-medium transition-colors ${
                  currentSource === source.id
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                <div className="flex items-center space-x-1 sm:space-x-2">
                  <Monitor className="h-4 w-4 flex-shrink-0" />
                  <span className="hidden sm:inline">{source.name}</span>
                  <span className="text-xs opacity-75">{source.quality}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* 集数列表 */}
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="text-white text-lg font-semibold mb-3">
            剧集列表 ({mockEpisodes.length}集)
            <span className="text-sm text-gray-400 ml-2">当前第 {currentEpisode} 集</span>
          </h3>
          <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10 xl:grid-cols-12 gap-2">
            {mockEpisodes.map((episode) => (
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