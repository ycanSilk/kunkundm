// 简单的数据存储，用于模拟爬虫数据
export const crawlerStore = {
  // 获取动漫列表
  getAnimeList: () => {
    return [
      {
        id: '1',
        title: '葬送的芙莉莲',
        titleEn: 'Frieren: Beyond Journey\'s End',
        episodes: 28,
        coverImage: 'https://via.placeholder.com/400x600/8B5CF6/FFFFFF?text=葬送的芙莉莲',
        description: '打倒魔王的勇者一行人的后日谈——',
        fullDescription: '打倒魔王的勇者一行人的后日谈——\n\n打倒魔王「之后」的物语。\n\n打倒魔王的勇者一行人的后日谈——\n\n打倒魔王「之后」的物语。\n\n寿命论与人性探讨的奇幻故事。',
        type: 'TV动画',
        year: 2023,
        season: '秋季',
        studio: 'MADHOUSE',
        genres: ['奇幻', '冒险', '剧情'],
        rating: 9.2,
        duration: '24分钟/集',
        status: '已完结',
        broadcastDay: '周五',
        episodesList: Array.from({ length: 28 }, (_, i) => ({
          id: i + 1,
          title: `第${i + 1}集`,
          duration: '24分钟',
          airDate: `2023年${Math.floor(i / 4) + 9}月${(i % 4) * 7 + 1}日`,
          thumbnail: `https://via.placeholder.com/300x200/8B5CF6/FFFFFF?text=EP${i + 1}`,
          description: `葬送的芙莉莲 第${i + 1}集`,
          videoUrl: `http://example.com/video/${i + 1}`
        }))
      },
      {
        id: '2',
        title: '迷宫饭',
        titleEn: 'Delicious in Dungeon',
        episodes: 24,
        coverImage: 'https://via.placeholder.com/400x600/10B981/FFFFFF?text=迷宫饭',
        description: '在迷宫中吃魔物的奇幻冒险。',
        fullDescription: '在一次迷宫探索中，莱欧斯的妹妹法琳被红龙吞食。为了拯救妹妹，莱欧斯决定再次挑战迷宫，但这次他选择吃迷宫中的魔物来节省粮食。',
        type: 'TV动画',
        year: 2024,
        season: '冬季',
        studio: 'Studio TRIGGER',
        genres: ['奇幻', '冒险', '美食'],
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
          description: `迷宫饭 第${i + 1}集`,
          videoUrl: `http://example.com/video/${i + 1}`
        }))
      }
    ];
  },

  // 获取每周更新
  getWeeklyUpdates: () => {
    return [
      {
        day: '周一',
        anime: ['无职转生', '关于我转生变成史莱姆这档事']
      },
      {
        day: '周二',
        anime: ['间谍过家家', '鬼灭之刃']
      },
      {
        day: '周三',
        anime: ['进击的巨人', '咒术回战']
      },
      {
        day: '周四',
        anime: ['迷宫饭', '葬送的芙莉莲']
      },
      {
        day: '周五',
        anime: ['葬送的芙莉莲', '无职转生']
      },
      {
        day: '周六',
        anime: ['鬼灭之刃', '间谍过家家']
      },
      {
        day: '周日',
        anime: ['进击的巨人', '咒术回战']
      }
    ];
  },

  // 搜索动漫
  getSearchResults: (query: string) => {
    const allAnime = crawlerStore.getAnimeList();
    if (!query) return allAnime;
    
    return allAnime.filter(anime => 
      anime.title.toLowerCase().includes(query.toLowerCase()) ||
      anime.titleEn.toLowerCase().includes(query.toLowerCase()) ||
      anime.genres.some(genre => genre.toLowerCase().includes(query.toLowerCase()))
    );
  },

  // 获取最后更新时间
  getLastUpdated: () => {
    return new Date().toISOString();
  }
};