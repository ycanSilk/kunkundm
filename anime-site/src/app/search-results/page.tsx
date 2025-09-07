'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { Play, Search } from 'lucide-react';
import { Anime } from '@/types/anime';
import { Header } from '@/components/header';
import { Footer } from '@/components/footer';
import SearchInput from '@/components/search-input';

// 模拟数据
const mockAnimeData: Anime[] = [
  {
    id: '1',
    title: '葬送的芙莉莲',
    episodes: 28,
    coverImage: 'https://via.placeholder.com/300x400/8B5CF6/FFFFFF?text=葬送的芙莉莲',
    description: '打倒魔王的勇者一行人的后日谈。精灵魔法使芙莉莲与勇者欣维尔、战士艾泽、僧侣海塔一起，经历了长达十年的打倒魔王的旅程。在魔王被打倒、世界恢复和平之后，芙莉莲为了理解人类的情感，开始了新的旅程。',
    type: 'TV动画',
    year: 2023
  },
  {
    id: '2',
    title: '迷宫饭',
    episodes: 24,
    coverImage: 'https://via.placeholder.com/300x400/10B981/FFFFFF?text=迷宫饭',
    description: '在迷宫中吃魔物的奇幻冒险。为了救回被红龙吃掉的妹妹法琳，莱奥斯一行人必须在迷宫中前进。但是食物已经吃完了...于是，他们决定吃迷宫中的魔物！',
    type: 'TV动画',
    year: 2024
  },
  {
    id: '3',
    title: '怪兽8号',
    episodes: 12,
    coverImage: 'https://via.placeholder.com/300x400/F59E0B/FFFFFF?text=怪兽8号',
    description: '人类与怪兽的战斗故事。在日本这个怪兽出现率世界第一的国家里，怪兽防卫队日复一日地与怪兽战斗着。在垃圾处理厂工作的青年日比野卡夫卡，某天突然变成了怪兽...',
    type: 'TV动画',
    year: 2024
  },
  {
    id: '4',
    title: '无职转生～到了异世界就拿出真本事～',
    episodes: 23,
    coverImage: 'https://via.placeholder.com/300x400/EF4444/FFFFFF?text=无职转生',
    description: '异世界转生冒险故事。34岁的尼特族在身无分文的情况下被赶出家门，发现自己的人生已经走进了完全的绝路。才刚刚感到后悔，他就被卡车撞死了。然后，他转生到了剑与魔法的异世界！',
    type: 'TV动画',
    year: 2021
  },
  {
    id: '5',
    title: '间谍过家家',
    episodes: 25,
    coverImage: 'https://via.placeholder.com/300x400/3B82F6/FFFFFF?text=间谍过家家',
    description: '间谍家庭的喜剧日常。西国能力最强的间谍<黄昏>，为了执行某个任务而被命令组建家庭。但是，他的女儿安妮亚是超能力者，妻子约尔是杀手！互相隐藏真实身份的临时家庭，展开了一场充满欢笑的家庭喜剧。',
    type: 'TV动画',
    year: 2022
  },
  {
    id: '6',
    title: '鬼灭之刃',
    episodes: 26,
    coverImage: 'https://via.placeholder.com/300x400/DC2626/FFFFFF?text=鬼灭之刃',
    description: '大正时期的猎鬼故事。卖炭少年炭治郎，某天家人被鬼杀害，妹妹祢豆子变成了鬼。为了让妹妹变回人类，为了消灭杀害家人的鬼，炭治郎踏上了斩鬼之旅。',
    type: 'TV动画',
    year: 2019
  },
  {
    id: '7',
    title: '进击的巨人',
    episodes: 75,
    coverImage: 'https://via.placeholder.com/300x400/1F2937/FFFFFF?text=进击的巨人',
    description: '人类与巨人的生存之战。107年前，世界上突然出现了巨人，人类被逼到了灭绝的边缘。幸存下来的人类建造了三重巨大的防护墙，在这隔绝的环境里享受了一百多年的和平。',
    type: 'TV动画',
    year: 2013
  },
  {
    id: '8',
    title: '我的英雄学院',
    episodes: 138,
    coverImage: 'https://via.placeholder.com/300x400/7C3AED/FFFFFF?text=我的英雄学院',
    description: '超能力社会的英雄故事。在这个80%的人类都拥有某种被称为"个性"的超能力的世界里，天生没有"个性"的少年绿谷出久，以成为职业英雄为目标，进入了雄英高中英雄科。',
    type: 'TV动画',
    year: 2016
  }
];

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
      
      // 模拟搜索延迟
      setTimeout(() => {
        const filtered = mockAnimeData.filter(anime =>
          anime.title.toLowerCase().includes(query.toLowerCase()) ||
          anime.description.toLowerCase().includes(query.toLowerCase()) ||
          anime.type.toLowerCase().includes(query.toLowerCase())
        );
        setSearchResults(filtered);
        setLoading(false);
      }, 800);
    } else {
      setSearchResults(mockAnimeData);
      setLoading(false);
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