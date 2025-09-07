"use client"

import { YearlyAnimeList } from "@/components/yearly-anime-list"
import { Anime } from "@/types/anime"

// 模拟年份动漫数据
const mockYearlyData: { [key: string]: Anime[] } = {
  "2024": [
    {
      id: "1",
      title: "葬送的芙莉莲",
      episode: "第28集",
      description: "打倒魔王的勇者一行人的魔法使芙莉莲，在勇者死后，开始了新的旅程。",
      coverImage: "https://via.placeholder.com/300x400/8B5CF6/FFFFFF?text=葬送的芙莉莲",
      genres: ["奇幻", "冒险"],
      rating: 9.5,
      releaseDate: "2024-01-05",
      url: "https://example.com/frieren"
    },
    {
      id: "2",
      title: "迷宫饭",
      episode: "第24集",
      description: "为了救回妹妹，冒险者莱欧斯决定吃迷宫里的魔物，开始了美食冒险。",
      coverImage: "https://via.placeholder.com/300x400/10B981/FFFFFF?text=迷宫饭",
      genres: ["奇幻", "美食"],
      rating: 9.2,
      releaseDate: "2024-01-04",
      url: "https://example.com/dungeon-meshi"
    },
    {
      id: "3",
      title: "怪兽8号",
      episode: "第12集",
      description: "在怪兽出现率最高的日本，32岁的男人日比野卡夫卡成为了怪兽。",
      coverImage: "https://via.placeholder.com/300x400/F59E0B/FFFFFF?text=怪兽8号",
      genres: ["动作", "科幻"],
      rating: 8.8,
      releaseDate: "2024-04-13",
      url: "https://example.com/kaiju-no8"
    },
    {
      id: "4",
      title: "无职转生",
      episode: "第23集",
      description: "34岁的尼特族转生到异世界，决定认真生活。",
      coverImage: "https://via.placeholder.com/300x400/EF4444/FFFFFF?text=无职转生",
      genres: ["奇幻", "冒险"],
      rating: 9.0,
      releaseDate: "2024-10-07",
      url: "https://example.com/mushoku-tensei"
    }
  ],
  "2023": [
    {
      id: "5",
      title: "鬼灭之刃 刀匠村篇",
      episode: "第11集",
      description: "炭治郎前往刀匠村，与霞柱无一郎和恋柱甘露寺一起战斗。",
      coverImage: "https://via.placeholder.com/300x400/EC4899/FFFFFF?text=鬼灭之刃",
      genres: ["动作", "奇幻"],
      rating: 9.3,
      releaseDate: "2023-04-09",
      url: "https://example.com/kimetsu-swordsmith"
    },
    {
      id: "6",
      title: "咒术回战 第二季",
      episode: "第23集",
      description: "五条悟的过去篇，以及涩谷事变的开始。",
      coverImage: "https://via.placeholder.com/300x400/6366F1/FFFFFF?text=咒术回战",
      genres: ["动作", "超自然"],
      rating: 9.1,
      releaseDate: "2023-07-06",
      url: "https://example.com/jujutsu-kaisen-s2"
    },
    {
      id: "7",
      title: "间谍过家家",
      episode: "第25集",
      description: "间谍黄昏为了任务组成了虚假家庭，却不知道妻子是杀手，女儿是超能力者。",
      coverImage: "https://via.placeholder.com/300x400/06B6D4/FFFFFF?text=间谍过家家",
      genres: ["喜剧", "动作"],
      rating: 9.4,
      releaseDate: "2023-10-07",
      url: "https://example.com/spy-family"
    }
  ],
  "2022": [
    {
      id: "8",
      title: "孤独摇滚！",
      episode: "第12集",
      description: "社恐少女后藤一里在机缘巧合下成为了乐队吉他手。",
      coverImage: "https://via.placeholder.com/300x400/F97316/FFFFFF?text=孤独摇滚",
      genres: ["音乐", "喜剧"],
      rating: 9.2,
      releaseDate: "2022-10-08",
      url: "https://example.com/bocchi-the-rock"
    },
    {
      id: "9",
      title: "电锯人",
      episode: "第12集",
      description: "贫穷少年淀治与链锯恶魔啵奇塔一起成为了恶魔猎人。",
      coverImage: "https://via.placeholder.com/300x400/84CC16/FFFFFF?text=电锯人",
      genres: ["动作", "恐怖"],
      rating: 8.9,
      releaseDate: "2022-10-12",
      url: "https://example.com/chainsaw-man"
    }
  ],
  "2021": [
    {
      id: "10",
      title: "86-不存在的战区-",
      episode: "第23集",
      description: "少年少女们驾驶着无人战斗机，为了守护祖国而战。",
      coverImage: "https://via.placeholder.com/300x400/D946EF/FFFFFF?text=86",
      genres: ["科幻", "战争"],
      rating: 8.8,
      releaseDate: "2021-04-10",
      url: "https://example.com/86"
    },
    {
      id: "11",
      title: "奇巧计程车",
      episode: "第13集",
      description: "看似普通的出租车司机小户川，卷入了奇妙的案件中。",
      coverImage: "https://via.placeholder.com/300x400/14B8A6/FFFFFF?text=奇巧计程车",
      genres: ["悬疑", "剧情"],
      rating: 9.1,
      releaseDate: "2021-04-06",
      url: "https://example.com/odd-taxi"
    }
  ],
  "2020": [
    {
      id: "12",
      title: "咒术回战",
      episode: "第24集",
      description: "高中生虎杖悠仁为了拯救他人，吞下了特级咒物。",
      coverImage: "https://via.placeholder.com/300x400/8B5CF6/FFFFFF?text=咒术回战",
      genres: ["动作", "超自然"],
      rating: 8.7,
      releaseDate: "2020-10-03",
      url: "https://example.com/jujutsu-kaisen"
    }
  ],
  "2019": [
    {
      id: "13",
      title: "鬼灭之刃",
      episode: "第26集",
      description: "少年炭治郎为了拯救变成鬼的妹妹，加入了鬼杀队。",
      coverImage: "https://via.placeholder.com/300x400/EF4444/FFFFFF?text=鬼灭之刃",
      genres: ["动作", "奇幻"],
      rating: 8.9,
      releaseDate: "2019-04-06",
      url: "https://example.com/kimetsu-yaiba"
    }
  ],
  "2018": [
    {
      id: "14",
      title: "紫罗兰永恒花园",
      episode: "第13集",
      description: "战争结束后，少女薇欧瑞特成为了自动手记人偶，寻找爱的意义。",
      coverImage: "https://via.placeholder.com/300x400/8B5CF6/FFFFFF?text=紫罗兰永恒花园",
      genres: ["剧情", "治愈"],
      rating: 9.0,
      releaseDate: "2018-01-10",
      url: "https://example.com/violet-evergarden"
    }
  ]
}

export default function YearlyListPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <YearlyAnimeList yearlyData={mockYearlyData} />
    </div>
  )
}