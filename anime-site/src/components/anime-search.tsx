'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';

interface Anime {
  id: string;
  title: string;
  episodes: number;
  coverImage?: string;
  description?: string;
  type?: string;
  year?: number;
}

interface AnimeSearchProps {
  onSearch: (query: string) => void;
  results?: Anime[];
  loading?: boolean;
  placeholder?: string;
}

export default function AnimeSearch({ 
  onSearch, 
  results = [], 
  loading = false,
  placeholder = "搜索动漫名称..."
}: AnimeSearchProps) {
  const [query, setQuery] = useState('');
  const [showResults, setShowResults] = useState(false);

  const handleSearch = (value: string) => {
    setQuery(value);
    if (value.trim()) {
      onSearch(value);
      setShowResults(true);
    } else {
      setShowResults(false);
    }
  };

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (query.trim()) {
      window.location.href = `/search-results?q=${encodeURIComponent(query)}`;
    }
  };

  const handleResultClick = (anime: Anime) => {
    setQuery(anime.title);
    setShowResults(false);
    // 这里可以添加跳转到详情页的逻辑
    console.log('Selected anime:', anime);
  };

  return (
    <div className="relative w-full max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder={placeholder}
          className="block w-full pl-4 pr-10 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
        />
        <button
          type="submit"
          className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
        >
          <Search className="h-5 w-5" />
        </button>
      </form>

      {showResults && (
        <div className="absolute z-10 mt-2 w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto">
          {loading ? (
            <div className="px-4 py-3 text-center text-gray-500">
              搜索中...
            </div>
          ) : results.length > 0 ? (
            <ul className="divide-y divide-gray-200">
              {results.map((anime) => (
                <li key={anime.id}>
                  <button
                    onClick={() => handleResultClick(anime)}
                    className="w-full px-4 py-3 hover:bg-gray-50 text-left transition-colors duration-150"
                  >
                    <div className="flex items-center space-x-3">
                      {anime.coverImage && (
                        <img
                          src={anime.coverImage}
                          alt={anime.title}
                          className="w-12 h-16 object-cover rounded"
                        />
                      )}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {anime.title}
                        </p>
                        <p className="text-sm text-gray-500">
                          {anime.episodes}集 {anime.type && `• ${anime.type}`}
                          {anime.year && `• ${anime.year}年`}
                        </p>
                      </div>
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          ) : query && (
            <div className="px-4 py-3 text-center text-gray-500">
              未找到相关动漫
            </div>
          )}
        </div>
      )}
    </div>
  );
}