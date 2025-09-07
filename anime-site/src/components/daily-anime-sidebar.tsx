"use client"

import * as React from "react"
import Link from 'next/link'
import { motion, AnimatePresence } from "framer-motion"
import { Anime } from "@/types/anime"

interface DailyAnimeSidebarProps {
  className?: string
}

interface RawAnimeData {
  name: string
  url: string
  episode: string
}

interface WeeklyUpdates {
  monday: RawAnimeData[]
  tuesday: RawAnimeData[]
  wednesday: RawAnimeData[]
  thursday: RawAnimeData[]
  friday: RawAnimeData[]
  saturday: RawAnimeData[]
  sunday: RawAnimeData[]
}

interface CrawlerData {
  updated_at: string
  source_url: string
  weekly_updates: WeeklyUpdates
}

const days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
const dayMapping: { [key: string]: keyof WeeklyUpdates } = {
  "周一": "monday",
  "周二": "tuesday", 
  "周三": "wednesday",
  "周四": "thursday",
  "周五": "friday",
  "周六": "saturday",
  "周日": "sunday"
}

export function DailyAnimeSidebar({ className }: DailyAnimeSidebarProps) {
  const [weeklyData, setWeeklyData] = React.useState<{ [key: string]: Anime[] }>({})
  const [activeDay, setActiveDay] = React.useState("周一")
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    loadDailyUpdates()
  }, [])

  const loadDailyUpdates = async () => {
    try {
      const response = await fetch('/crawler_daily_update.json')
      if (!response.ok) {
        throw new Error('无法加载数据')
      }
      
      const data: CrawlerData = await response.json()
      
      // 转换数据结构
      const formattedData: { [key: string]: Anime[] } = {}
      
      days.forEach(day => {
        const dayKey = dayMapping[day]
        const rawAnimeList = data.weekly_updates[dayKey] || []
        
        formattedData[day] = rawAnimeList.map((anime, index) => {
          // 从URL中提取动漫ID，例如从 http://www.iyinghua.com/show/6462.html 提取 6462
          const urlMatch = anime.url.match(/\/show\/(\d+)\.html/)
          const animeId = urlMatch ? urlMatch[1] : `${day}-${index}`
          
          return {
            id: animeId,
            title: anime.name,
            url: anime.url,
            episode: anime.episode,
            thumbnail: '',
            description: ''
          }
        })
      })
      
      setWeeklyData(formattedData)
      setLoading(false)
    } catch (error) {
      console.error('加载每日更新数据失败:', error)
      setLoading(false)
    }
  }

  const currentAnimeList = weeklyData[activeDay] || []

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-sm ${className || ''}`}>
        <div className="border-b border-gray-200 px-3 sm:px-4 py-3">
          <h3 className="text-xl sm:text-2xl font-semibold text-gray-900">每日更新</h3>
        </div>
        <div className="p-6 text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-2 text-sm text-gray-500">加载中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm ${className || ''}`}>
      {/* 标题 */}
      <div className="border-b border-gray-200 px-3 sm:px-4 py-3">
        <h3 className="text-xl sm:text-2xl font-semibold text-gray-900">每日更新</h3>
      </div>

      {/* 星期选择 */}
      <div className="border-b border-gray-200 p-2">
        <div className="grid grid-cols-4 sm:grid-cols-7 gap-1">
          {days.map((day) => (
            <button
              key={day}
              onClick={() => setActiveDay(day)}
              className={`px-1 py-2 text-xs font-medium rounded-md border transition-all duration-200 transform hover:scale-105 hover:shadow-sm ${
                activeDay === day
                  ? 'bg-purple-600 text-white border-purple-600 shadow-md'
                  : 'text-gray-600 bg-white border-gray-300 hover:bg-purple-50 hover:border-purple-300 hover:text-purple-700'
              }`}
            >
              {day}
            </button>
          ))}
        </div>
      </div>

      {/* 动漫列表 - 适合侧边栏的紧凑布局 */}
      <div className="pb-60 pt-3 px-3 ">
        <AnimatePresence mode="wait">
          {currentAnimeList.length > 0 ? (
            <motion.div
              key={activeDay}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <ul className="space-y-2">
                {currentAnimeList.slice(0, 8).map((anime, index) => (
                  <motion.li
                    key={anime.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.03 }}
                    className="group flex items-center justify-between rounded-md bg-gray-50 px-2 py-2 transition-colors hover:bg-gray-100"
                  >
                    <div className="flex-1 min-w-0">
                      <Link
                        href={`/anime/${anime.id}`}
                        className="text-sm font-medium text-gray-900 hover:text-purple-600 transition-colors truncate block"
                      >
                        {anime.title}
                      </Link>
                    </div>
                    <div className="ml-2 flex-shrink-0">
                      <span className="inline-flex items-center rounded-full bg-purple-100 px-2 py-0.5 text-xs font-medium text-purple-800">
                        {anime.episode}
                      </span>
                    </div>
                  </motion.li>
                ))}
              </ul>
            </motion.div>
          ) : (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="py-6 text-center"
            >
              <p className="text-sm text-gray-500">
                {activeDay} 暂无更新
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}