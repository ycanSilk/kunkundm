'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Play, Calendar, Film, Clock, Star, ChevronRight } from 'lucide-react';
import { Header } from '@/components/header';
import { Footer } from '@/components/footer';
import { Anime } from '@/types/anime';

// 模拟数据 - 实际项目中会从API获取
const mockAnimeDetails: Record<string, any> = {
  '1': {
    id: '1',
    title: '葬送的芙莉莲',
    titleEn: 'Frieren: Beyond Journey\'s End',
    episodes: 28,
    coverImage: 'https://via.placeholder.com/400x600/8B5CF6/FFFFFF?text=葬送的芙莉莲',
    description: '打倒魔王的勇者一行人的后日谈。打倒魔王后，世界恢复了和平。芙莉莲作为精灵，拥有近乎无限的寿命，她决定踏上新的旅程，去理解人类的情感。',
    fullDescription: '精灵魔法使芙莉莲与勇者辛美尔等人一起，历经十年的冒险，打败了魔王，为世界带来了和平。作为长命种精灵的芙莉莲，在与辛美尔等人分别后，独自踏上了收集魔法的旅程。五十年后，芙莉莲再次拜访了辛美尔，但辛美尔已经老去，生命所剩无几。在辛美尔的葬礼上，芙莉莲对自己过去未能了解人类产生了后悔。于是，她决定再次踏上旅程，去了解人类的情感。',
    type: 'TV动画',
    year: 2023,
    season: '秋季',
    studio: 'MADHOUSE',
    genres: ['奇幻', '冒险', '剧情', '治愈'],
    rating: 9.5,
    duration: '24分钟/集',
    status: '已完结',
    broadcastDay: '周五',
    episodesList: Array.from({ length: 28 }, (_, i) => ({
      id: i + 1,
      title: `第${i + 1}集`,
      duration: '24分钟',
      airDate: `2023年${Math.floor(i / 4) + 9}月${(i % 4) * 7 + 1}日`,
      thumbnail: `https://via.placeholder.com/300x200/8B5CF6/FFFFFF?text=EP${i + 1}`,
      description: `葬送的芙莉莲 第${i + 1}集`
    }))
  },
  '2': {
    id: '2',
    title: '迷宫饭',
    titleEn: 'Delicious in Dungeon',
    episodes: 24,
    coverImage: 'https://via.placeholder.com/400x600/10B981/FFFFFF?text=迷宫饭',
    description: '在迷宫中吃魔物的奇幻冒险。为了拯救被龙吞食的妹妹，莱欧斯决定再次挑战迷宫，但这次他选择吃迷宫中的魔物来节省粮食。',
    fullDescription: '在一次迷宫探索中，莱欧斯的妹妹法琳被红龙吞食。为了拯救妹妹，莱欧斯决定再次挑战迷宫。但是，由于之前的失败，队伍已经解散，资金也所剩无几。于是，莱欧斯决定吃迷宫中的魔物来节省粮食。在迷宫中，他们遇到了各种奇特的魔物，并用它们制作了美味的料理。',
    type: 'TV动画',
    year: 2024,
    season: '冬季',
    studio: 'Studio TRIGGER',
    genres: ['奇幻', '冒险', '美食', '喜剧'],
    rating: 8.8,
    duration: '24分钟/集',
    status: '已完结',
    broadcastDay: '周四',
    episodesList: Array.from({ length: 24 }, (_, i) => ({
      id: i + 1,
      title: `第${i + 1}集`,
      duration: '24分钟',
      airDate: `2024年${Math.floor(i / 4) + 1}月${(i % 4) * 7 + 1}日`,
      thumbnail: `https://via.placeholder.com/300x200/10B981/FFFFFF?text=EP${i + 1}`,
      description: `迷宫饭 第${i + 1}集`
    }))
  }
};

export default function AnimeDetailPage() {
  const params = useParams();
  const [anime, setAnime] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedEpisode, setSelectedEpisode] = useState(1);

  useEffect(() => {
    const animeId = params.id as string;
    if (animeId) {
      setLoading(true);
      // 从URL参数中获取动漫ID并调用API获取真实数据
      fetch(`/api/anime/${animeId}`)
        .then(res => res.json())
        .then(response => {
          if (response.success && response.data) {
            setAnime(response.data);
          } else {
            // 如果API返回错误，使用模拟数据
            setAnime(mockAnimeDetails['1']);
          }
          setLoading(false);
        })
        .catch(() => {
          // 如果API调用失败，使用模拟数据
          setTimeout(() => {
            setAnime(mockAnimeDetails['1']);
            setLoading(false);
          }, 1000);
        });
    }
  }, [params?.id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
              <p className="mt-4 text-lg text-gray-600">加载中...</p>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (!anime) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center py-12">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">动漫未找到</h1>
            <p className="text-gray-600">请返回首页或尝试其他动漫</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* 动漫详情头部 */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="flex flex-col lg:flex-row">
            {/* 封面图片 */}
            <div className="lg:w-1/3 w-full">
              <img
                src={anime.coverImage}
                alt={anime.title}
                className="w-full h-64 sm:h-80 md:h-96 lg:h-full object-cover"
              />
            </div>
            
            {/* 详情信息 */}
            <div className="lg:w-2/3 w-full p-4 sm:p-6 lg:p-8">
              <div className="mb-3">
                <h2 className="text-3xl lg:text-4xl font-bold text-gray-900">
                  {anime.title}
                </h2>

              </div>

              <div className="flex flex-col sm:flex-row sm:flex-wrap gap-4 mb-3">
                <div className="flex items-center">
                  <Calendar className="h-4 w-4 text-blue-400 mr-1.5 flex-shrink-0" />
                  <span className="text-gray-700 text-sm">上映时间：{anime.year}</span>
                </div>
                <div className="flex items-center">
                  <Clock className="h-4 w-4 text-green-400 mr-1.5 flex-shrink-0" />
                  <span className="text-gray-700 text-sm">集数：{anime.episodes}集</span>
                </div>
                <div className="flex flex-col sm:flex-row items-start sm:items-center">
                  <div className="flex items-center mb-2 sm:mb-0 sm:mr-3">
                    <Film className="h-4 w-4 text-purple-400 mr-1.5 flex-shrink-0" />
                    <span className="text-gray-700 font-medium text-sm">类型：</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {anime.genres.map((genre: string, index: number) => (
                      <span key={index} className="px-2 py-0.5 bg-purple-100 text-purple-800 rounded-full text-xs">
                        {genre}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
              <div className="mb-3">
                <h3 className="text-lg font-semibold text-gray-900 mb-1">介绍：</h3>
                <p className="text-gray-700 leading-relaxed">
                  {anime.fullDescription}
                </p>
              </div>
              <button 
                onClick={() => window.location.href = `/watch/${anime.id}`}
                className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center"
              >
                <Play className="h-5 w-5 mr-2" />
                开始观看
              </button>
            </div>
          </div>
        </div>

        {/* 集数列表 */}
        <div className="mt-8 ">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              集数列表 ({anime.episodes}集)
            </h3>
            
            <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 xl:grid-cols-8 gap-2">
                {anime.episodesList.map((episode: any) => (
                  <a
                    key={episode.id}
                    href={`/watch/${anime.id}?episode=${episode.id}`}
                    className={`block border rounded text-center cursor-pointer transition-all duration-300 hover:shadow-md hover:bg-gray-50 ${
                      selectedEpisode === episode.id
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-200 hover:border-purple-300'
                    }`}
                  >
                    <div className="p-2">
                      <div className="text-xs sm:text-sm font-medium text-gray-700 transition-colors duration-300 hover:text-purple-700">
                        第{episode.id}集
                      </div>
                    </div>
                  </a>
                ))}
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}