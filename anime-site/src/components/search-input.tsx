'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';

interface SearchInputProps {
  placeholder?: string;
  initialValue?: string;
  onSearch?: (query: string) => void;
  className?: string;
}

export default function SearchInput({ 
  placeholder = "搜索动漫名称、类型或描述...",
  initialValue = "",
  onSearch,
  className = ""
}: SearchInputProps) {
  const [searchValue, setSearchValue] = useState(initialValue);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(searchValue.trim());
    } else {
      // 默认行为：跳转到搜索结果页面
      if (searchValue.trim()) {
        window.location.href = `/search-results?q=${encodeURIComponent(searchValue.trim())}`;
      } else {
        window.location.href = '/search-results';
      }
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value);
  };

  return (
    <form onSubmit={handleSubmit} className={`relative ${className}`}>
      <input
        type="text"
        value={searchValue}
        onChange={handleInputChange}
        placeholder={placeholder}
        className="block w-full pl-4 pr-10 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
      />
      <button
        type="submit"
        className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-purple-600 transition-colors duration-200"
      >
        <Search className="h-5 w-5" />
      </button>
    </form>
  );
}