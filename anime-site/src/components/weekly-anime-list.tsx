"use client"

import * as React from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Anime } from "@/types/anime"

interface WeeklyAnimeListProps {
  weeklyData: {
    [key: string]: Anime[]
  }
  className?: string
}

const days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

export function WeeklyAnimeList({ weeklyData, className }: WeeklyAnimeListProps) {
  const [activeDay, setActiveDay] = React.useState("周一")

  const currentAnimeList = weeklyData[activeDay] || []

  return (
    <div className={`min-h-screen bg-gray-50 py-8 ${className || ''}`}>
      <div className="mx-auto max-w-2xl px-4 sm:px-6 lg:px-8">
        {/* Tab切换栏 */}
        <div className="mb-6">
          <div className="flex space-x-1 overflow-x-auto rounded-lg bg-white p-1 shadow-sm">
            {days.map((day) => (
              <button
                key={day}
                onClick={() => setActiveDay(day)}
                className={`relative flex-shrink-0 rounded-md px-4 py-2 text-sm font-medium transition-all duration-200 ${
                  activeDay === day
                    ? 'bg-purple-600 text-white shadow-md'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
>
                {day}
              </button>
            ))}
          </div>
        </div>

        {/* 动漫列表 - 极简布局：只保留名称和集数，左右分布 */}
        <AnimatePresence mode="wait">
          {currentAnimeList.length > 0 ? (
            <motion.div
              key={activeDay}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <ul className="space-y-2">
                {currentAnimeList.map((anime, index) => (
                  <motion.li
                    key={anime.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="group flex items-center justify-between rounded-lg bg-white px-4 py-3 shadow-sm transition-all duration-200 hover:shadow-md"
                  >
                    <div className="flex-1 min-w-0">
                      <h3 className="text-base font-medium text-gray-900 truncate">
                        {anime.title}
                      </h3>
                    </div>
                    <div className="ml-4 flex-shrink-0">
                      <span className="inline-flex items-center rounded-full bg-purple-100 px-3 py-1 text-sm font-medium text-purple-800">
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
              className="py-12 text-center"
            >
              <div className="mx-auto h-16 w-16 rounded-full bg-gray-100 flex items-center justify-center">
                <span className="text-gray-400 text-sm">暂无</span>
              </div>
              <p className="mt-3 text-sm text-gray-500">
                {activeDay} 暂无动漫更新
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}