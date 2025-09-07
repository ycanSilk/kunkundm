"use client"

import * as React from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Anime } from "@/types/anime"

interface YearlyAnimeListProps {
  yearlyData: {
    [key: string]: Anime[]
  }
  className?: string
}

const years = ["2025","2024", "2023", "2022", "2021", "2020", "2019", "2018","2017","2016","2015",
  "2014","2013","2012","2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000"]

export function YearlyAnimeList({ yearlyData, className }: YearlyAnimeListProps) {
  const [activeYear, setActiveYear] = React.useState("2024")

  const currentAnimeList = yearlyData[activeYear] || []

  return (
    <div className={`min-h-screen bg-gray-50 py-8 ${className || ''}`}>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* 年份选择 - 分行显示，每行10个年份，响应式布局 */}
        <div className="mb-6">
          <div className="rounded-lg bg-white p-3 shadow-sm">
            <div className="grid grid-cols-5 sm:grid-cols-7 md:grid-cols-10 gap-2">
              {years.map((year) => (
                <button
                  key={year}
                  onClick={() => setActiveYear(year)}
                  className={`relative rounded-md px-2 py-2 text-sm font-medium transition-all duration-200 whitespace-nowrap ${
                    activeYear === year
                      ? 'bg-purple-600 text-white shadow-md'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
>
                  {year}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* 动漫卡片网格 */}
        <AnimatePresence mode="wait">
          {currentAnimeList.length > 0 ? (
            <motion.div
              key={activeYear}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {currentAnimeList.map((anime, index) => (
                  <motion.div
                    key={anime.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="group bg-white rounded-lg shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden"
                  >
                    {/* 动漫封面 */}
                    <div className="aspect-[3/4] bg-gray-200 overflow-hidden">
                      {anime.coverImage ? (
                        <img
                          src={anime.coverImage}
                          alt={anime.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-100 to-pink-100">
                          <span className="text-gray-500 text-sm">暂无封面</span>
                        </div>
                      )}
                    </div>

                    {/* 动漫信息 */}
                    <div className="p-4">
                      {/* 动漫名称 */}
                      <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                        {anime.title}
                      </h3>

                      {/* 动漫介绍 */}
                      <p className="text-sm text-gray-600 mb-3 line-clamp-3">
                        {anime.description || "暂无介绍"}
                      </p>

                      {/* 集数和类型 */}
                      <div className="flex items-center justify-between">
                        <span className="inline-flex items-center rounded-full bg-purple-100 px-2.5 py-1 text-xs font-medium text-purple-800">
                          {anime.episode}
                        </span>
                        <div className="flex flex-wrap gap-1">
                          {anime.genres.slice(0, 2).map((genre) => (
                            <span
                              key={genre}
                              className="inline-flex items-center rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-700"
                            >
                              {genre}
                            </span>
                          ))}
                          {anime.genres.length > 2 && (
                            <span className="text-xs text-gray-500">+{anime.genres.length - 2}</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
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
                {activeYear} 年暂无动漫数据
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}