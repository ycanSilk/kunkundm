'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { Play, Search } from 'lucide-react';
import { Anime } from '@/types/anime';
import { Header } from '@/components/header';
import { Footer } from '@/components/footer';
import SearchInput from '@/components/search-input';

// 真实数据将通过API获取

export default function SearchResultsPage() {
  const searchParams = useSearchParams();
  const [searchResults, setSearchResults] = useState<Anime[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const query = searchParams.get('q') || '';
    setSearchQuery(query);
    
    if (query) {
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
    } else {
      // 空查询时获取所有动漫
      fetch('/api/anime?action=list')
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
          console.error('获取动漫列表失败:', error);
          setSearchResults([]);
          setLoading(false);
        });
    }
  }, [searchParams]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
            <p className="mt-4 text-lg text-gray-600">正在搜索中...</p>
            <p className="mt-2 text-sm text-gray-500">请稍候</p>
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
        {/* 搜索框 - 居中显示 */}
        <div className="mb-6">
          <SearchInput
            initialValue={searchQuery}
            placeholder="搜索动漫名称、类型或描述..."
            className="max-w-2xl mx-auto"
          />
        </div>

        {/* 搜索关键词和结果数量 - 同一行显示 */}
        {searchQuery && (
          <div className="mb-6 text-center">
            <span className="text-lg font-medium text-gray-900">
              "{searchQuery}"
            </span>
            <span className="text-gray-600 ml-2">
              的搜索结果 ({searchResults.length} 个)
            </span>
          </div>
        )}
        
        {!searchQuery && searchResults.length > 0 && (
          <div className="mb-6 text-center">
            <span className="text-lg font-medium text-gray-900">
              所有动漫
            </span>
            <span className="text-gray-600 ml-2">
              ({searchResults.length} 个)
            </span>
          </div>
        )}

        {/* 搜索结果列表 */}
        <div className="space-y-4">
          {searchResults.map((anime) => (
            <a
              key={anime.id}
              href={`/anime/${anime.id}`}
              className="block bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
            >
              <div className="flex">
                {/* 封面图片 */}
                <div className="flex-shrink-0">
                  <img
                    src={anime.coverImage}
                    alt={anime.title}
                    className="w-40 h-60 object-cover"
                  />
                </div>
                
                {/* 内容信息 */}
                <div className="flex-1 p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        {anime.title}
                      </h2>
                      
                      <div className="flex items-center space-x-4 mb-3">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                          {anime.type}
                        </span>
                        <span className="text-sm text-gray-600">
                          共 {anime.episodes} 集
                        </span>
                        <span className="text-sm text-gray-600">
                          {anime.year}年
                        </span>
                      </div>
                      
                      <p className="text-gray-700 leading-relaxed mb-4">
                        {anime.description}
                      </p>
                    </div>
                    
                    {/* 详情按钮 */}
                    <div className="flex-shrink-0 ml-4">
                      <div className="inline-flex items-center px-4 py-2 bg-purple-600 text-white text-sm font-medium rounded-md hover:bg-purple-700 transition-colors duration-200">
                        <Play className="h-4 w-4 mr-1" />
                        查看详情
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </a>
          ))}
        </div>

        {/* 无结果提示 */}
        {searchResults.length === 0 && (
          <div className="text-center py-12">
            <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {searchQuery ? `未找到与“${searchQuery}”相关的动漫` : '暂无动漫'}
            </h3>
            <p className="text-gray-600">
              {searchQuery ? '请检查关键词或尝试其他关键词' : '请稍后再试'}
            </p>
          </div>
        )}
      </div>
      
      <Footer />
    </div>
  );
}