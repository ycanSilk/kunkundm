"use client"

import { WeeklyAnimeList } from "@/components/weekly-anime-list"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Anime } from "@/types/anime"

// 模拟数据
const mockWeeklyData: { [key: string]: Anime[] } = {
  "周一": [
    {
      id: "1",
      title: "鬼灭之刃 柱训练篇",
      episode: "第8话",
      url: "#",
      rating: 9.2,
      releaseDate: "2024-04-01",
      genres: ["动作", "奇幻"],
      image: ""
    },
    {
      id: "2",
      title: "咒术回战 第二季",
      episode: "第21话",
      url: "#",
      rating: 9.5,
      releaseDate: "2024-04-01",
      genres: ["动作", "超自然"],
      image: ""
    },
    {
      id: "3",
      title: "进击的巨人 最终季",
      episode: "第28话",
      url: "#",
      rating: 9.8,
      releaseDate: "2024-04-01",
      genres: ["动作", "剧情"],
      image: ""
    }
  ],
  "周二": [
    {
      id: "4",
      title: "间谍过家家",
      episode: "第12话",
      url: "#",
      rating: 9.0,
      releaseDate: "2024-04-02",
      genres: ["喜剧", "动作"],
      image: ""
    },
    {
      id: "5",
      title: "辉夜大小姐想让我告白",
      episode: "第11话",
      url: "#",
      rating: 8.8,
      releaseDate: "2024-04-02",
      genres: ["喜剧", "校园"],
      image: ""
    }
  ],
  "周三": [
    {
      id: "6",
      title: "海贼王",
      episode: "第1100话",
      url: "#",
      rating: 9.3,
      releaseDate: "2024-04-03",
      genres: ["冒险", "动作"],
      image: ""
    },
    {
      id: "7",
      title: "我的英雄学院",
      episode: "第16话",
      url: "#",
      rating: 8.7,
      releaseDate: "2024-04-03",
      genres: ["动作", "校园"],
      image: ""
    }
  ],
  "周四": [
    {
      id: "8",
      title: "排球少年!!",
      episode: "第24话",
      url: "#",
      rating: 9.1,
      releaseDate: "2024-04-04",
      genres: ["运动", "校园"],
      image: ""
    }
  ],
  "周五": [
    {
      id: "9",
      title: "鬼灭之刃 刀匠村篇",
      episode: "第7话",
      url: "#",
      rating: 9.4,
      releaseDate: "2024-04-05",
      genres: ["动作", "奇幻"],
      image: ""
    },
    {
      id: "10",
      title: "JOJO的奇妙冒险",
      episode: "第9话",
      url: "#",
      rating: 9.0,
      releaseDate: "2024-04-05",
      genres: ["动作", "冒险"],
      image: ""
    }
  ],
  "周六": [
    {
      id: "11",
      title: "名侦探柯南",
      episode: "第1100话",
      url: "#",
      rating: 8.5,
      releaseDate: "2024-04-06",
      genres: ["推理", "悬疑"],
      image: ""
    },
    {
      id: "12",
      title: "咒术回战",
      episode: "第20话",
      url: "#",
      rating: 9.5,
      releaseDate: "2024-04-06",
      genres: ["动作", "超自然"],
      image: ""
    }
  ],
  "周日": [
    {
      id: "13",
      title: "间谍过家家 第二季",
      episode: "第10话",
      url: "#",
      rating: 9.1,
      releaseDate: "2024-04-07",
      genres: ["喜剧", "动作"],
      image: ""
    }
  ]
}

export default function WeeklyListPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <WeeklyAnimeList weeklyData={mockWeeklyData} />
      <Footer />
    </div>
  )
}