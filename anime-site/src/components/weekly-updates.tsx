"use client"

import * as React from "react"
import { motion } from "framer-motion"
import { Calendar, ChevronRight } from "lucide-react"
import { WeeklyUpdate } from "@/types/anime"
import { AnimeCard } from "@/components/anime-card"

interface WeeklyUpdatesProps {
  updates: WeeklyUpdate[]
}

export function WeeklyUpdates({ updates }: WeeklyUpdatesProps) {
  const dayColors = {
    "周一": "from-blue-500 to-blue-600",
    "周二": "from-green-500 to-green-600",
    "周三": "from-purple-500 to-purple-600",
    "周四": "from-yellow-500 to-yellow-600",
    "周五": "from-pink-500 to-pink-600",
    "周六": "from-indigo-500 to-indigo-600",
    "周日": "from-red-500 to-red-600"
  }

  return (
    <div className="space-y-8">
      {updates.map((dayUpdate, index) => (
        <motion.section
          key={dayUpdate.day}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
          className="rounded-xl bg-white p-6 shadow-lg"
        >
          <div className="mb-6 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className={`rounded-lg bg-gradient-to-r ${dayColors[dayUpdate.day as keyof typeof dayColors]} p-3 text-white`}>
                <Calendar className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{dayUpdate.day}</h2>
                <p className="text-sm text-gray-600">{dayUpdate.count} 部动漫更新</p>
              </div>
            </div>
            <ChevronRight className="h-5 w-5 text-gray-400" />
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
            {dayUpdate.anime.map((anime) => (
              <AnimeCard key={anime.id} anime={anime} />
            ))}
          </div>
        </motion.section>
      ))}
    </div>
  )
}