'use client';

import SearchInput from '@/components/search-input';

export default function HomeSearch() {
  return (
    <div className="bg-white py-8 sm:py-10 lg:py-12">
      <div className="mx-auto max-w-7xl px-3 sm:px-4 lg:px-6">
        <div className="text-center mb-6 sm:mb-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">
            搜索动漫
          </h2>
          <p className="text-base sm:text-lg text-gray-600">
            快速找到你想看的动漫
          </p>
        </div>
        
        <div className="relative max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl mx-auto">
          <SearchInput
            placeholder="输入动漫名称搜索..."
          />
        </div>
      </div>
    </div>
  );
}