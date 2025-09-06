import { Anime, WeeklyUpdate } from "@/types/anime"

export const mockAnimeData: Anime[] = [
  {
    id: "1",
    title: "鬼人幻灯抄",
    episode: "第21集",
    description: "以江户时代为背景的奇幻冒险故事",
    genres: ["奇幻", "冒险", "历史"],
    rating: 9.2,
    releaseDate: "2025-09-07",
    url: "http://www.iyinghua.com/v/6462-21.html"
  },
  {
    id: "2",
    title: "受到猩猩神的庇护的大小姐",
    episode: "第12集",
    description: "转生大小姐与猩猩神的奇妙冒险",
    genres: ["奇幻", "喜剧", "转生"],
    rating: 8.8,
    releaseDate: "2025-09-07",
    url: "http://www.iyinghua.com/v/6494-12.html"
  },
  {
    id: "3",
    title: "测不准的阿波连同学 第二季",
    episode: "第12集",
    description: "青春校园恋爱喜剧续作",
    genres: ["校园", "喜剧", "恋爱"],
    rating: 8.5,
    releaseDate: "2025-09-07",
    url: "http://www.iyinghua.com/v/6492-12.html"
  },
  {
    id: "4",
    title: "随兴旅-That’s Journey-",
    episode: "第12集",
    description: "轻松愉快的旅行日常故事",
    genres: ["日常", "治愈", "旅行"],
    rating: 8.3,
    releaseDate: "2025-09-07",
    url: "http://www.iyinghua.com/v/6487-12.html"
  },
  {
    id: "5",
    title: "夏日口袋",
    episode: "第22集",
    description: "夏日青春恋爱故事",
    genres: ["恋爱", "青春", "治愈"],
    rating: 9.0,
    releaseDate: "2025-09-08",
    url: "http://www.iyinghua.com/v/6490-22.html"
  },
  {
    id: "6",
    title: "正义使者 -我的英雄学院之非法英雄-",
    episode: "第13集",
    description: "我的英雄学院外传故事",
    genres: ["动作", "超能力", "热血"],
    rating: 8.7,
    releaseDate: "2025-09-08",
    url: "http://www.iyinghua.com/v/6491-13.html"
  },
  {
    id: "7",
    title: "机动战士高达 GQuuuuuuX",
    episode: "第12集",
    description: "高达系列最新作品",
    genres: ["机战", "科幻", "战争"],
    rating: 9.1,
    releaseDate: "2025-09-09",
    url: "http://www.iyinghua.com/v/6499-12.html"
  },
  {
    id: "8",
    title: "海贼王",
    episode: "第1141集",
    description: "经典热血冒险动漫",
    genres: ["冒险", "热血", "友情"],
    rating: 9.8,
    releaseDate: "2025-09-14",
    url: "http://www.iyinghua.com/v/2-1141.html"
  },
  {
    id: "9",
    title: "名侦探柯南",
    episode: "第1231集",
    description: "经典推理侦探动漫",
    genres: ["推理", "悬疑", "侦探"],
    rating: 9.5,
    releaseDate: "2025-09-13",
    url: "http://www.iyinghua.com/v/1412-1231.html"
  },
  {
    id: "10",
    title: "魔女守护者",
    episode: "第22集",
    description: "魔女与守护者的奇幻故事",
    genres: ["奇幻", "魔法", "冒险"],
    rating: 8.9,
    releaseDate: "2025-09-14",
    url: "http://www.iyinghua.com/v/6482-22.html"
  }
]

export const mockWeeklyUpdates: WeeklyUpdate[] = [
  {
    day: "周一",
    count: 7,
    anime: mockAnimeData.slice(0, 4)
  },
  {
    day: "周二",
    count: 7,
    anime: mockAnimeData.slice(4, 6)
  },
  {
    day: "周三",
    count: 7,
    anime: mockAnimeData.slice(6, 7)
  },
  {
    day: "周日",
    count: 14,
    anime: mockAnimeData.slice(7, 10)
  }
]