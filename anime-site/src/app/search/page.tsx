'use client';

import { useState } from 'react';
import AnimeSearch from '@/components/anime-search';
import { Anime } from '@/types/anime';

// 真实数据将通过API获取

export default function SearchPage() {
  const [searchResults, setSearchResults] = useState<Anime[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = (query: string) => {
    setLoading(true);
    
    // 调用真实API搜索
    fetch(`/api/anime?action=search&q=${encodeURIComponent(query)}`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setSearchResults(data.data);
        } else {
          setSearchResults([]);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error('搜索失败:', error);
        setSearchResults([]);
        setLoading(false);
      });
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