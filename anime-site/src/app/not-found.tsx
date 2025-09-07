import Link from 'next/link';
import { Home, Search } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="text-center">
        <div className="mb-8">
          <Search className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-900 mb-2">404</h1>
          <h2 className="text-xl font-medium text-gray-600 mb-4">页面未找到</h2>
          <p className="text-gray-500 max-w-md mx-auto">
            抱歉，您访问的页面不存在。可能是链接已失效或页面已被删除。
          </p>
        </div>
        
        <div className="space-y-4">
          <Link
            href="/"
            className="inline-flex items-center px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <Home className="h-5 w-5 mr-2" />
            返回首页
          </Link>
          
          <div className="text-sm text-gray-500">
            或者您可以尝试
            <Link href="/search-results" className="text-purple-600 hover:text-purple-700 ml-1">
              搜索动漫
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}