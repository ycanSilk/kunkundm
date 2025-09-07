'use client';

import { useState } from 'react';
import AnimeSearch from '@/components/anime-search';
import { Anime } from '@/types/anime';

// 模拟数据
const mockAnimeData: Anime[] = [
  {
    id: '1',
    title: '葬送的芙莉莲',
    episodes: 28,
    coverImage: 'https://via.placeholder.com/300x400/8B5CF6/FFFFFF?text=葬送的芙莉莲',
    description: '打倒魔王的勇者一行人的后日谈',
    type: 'TV',
    year: 2023
  },
  {
    id: '2',
    title: '迷宫饭',
    episodes: 24,
    coverImage: 'https://via.placeholder.com/300x400/10B981/FFFFFF?text=迷宫饭',
    description: '在迷宫中吃魔物的奇幻冒险',
    type: 'TV',
    year: 2024
  },
  {
    id: '3',
    title: '怪兽8号',
    episodes: 12,
    coverImage: 'https://via.placeholder.com/300x400/F59E0B/FFFFFF?text=怪兽8号',
    description: '人类与怪兽的战斗故事',
    type: 'TV',
    year: 2024
  },
  {
    id: '4',
    title: '无职转生',
    episodes: 23,
    coverImage: 'https://via.placeholder.com/300x400/EF4444/FFFFFF?text=无职转生',
    description: '异世界转生冒险故事',
    type: 'TV',
    year: 2021
  },
  {
    id: '5',
    title: '间谍过家家',
    episodes: 25,
    coverImage: 'https://via.placeholder.com/300x400/3B82F6/FFFFFF?text=间谍过家家',
    description: '间谍家庭的喜剧日常',
    type: 'TV',
    year: 2022
  }
];

export default function SearchPage() {
  const [searchResults, setSearchResults] = useState<Anime[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = (query: string) => {
    setLoading(true);
    
    // 模拟搜索延迟
    setTimeout(() => {
      const filtered = mockAnimeData.filter(anime =>
        anime.title.toLowerCase().includes(query.toLowerCase())
      );
      setSearchResults(filtered);
      setLoading(false);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">搜索动漫</h1>
          <p className="text-gray-600">输入动漫名称开始搜索</p>
        </div>

        <AnimeSearch 
          onSearch={handleSearch} 
          results={searchResults}
          loading={loading}
        />

        {searchResults.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">搜索结果</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {searchResults.map((anime) => (
                <div key={anime.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                  <img 
                    src={anime.coverImage} 
                    alt={anime.title}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="font-semibold text-gray-900 mb-1">{anime.title}</h3>
                    <p className="text-sm text-gray-600 mb-2">{anime.description}</p>
                    <div className="flex justify-between items-center text-sm text-gray-500">
                      <span>{anime.episodes}集</span>
                      <span>{anime.year}年</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}