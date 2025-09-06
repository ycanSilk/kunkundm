"use client"

import * as React from "react"
import { motion } from "framer-motion"
import { Play, TrendingUp, Calendar, Star } from "lucide-react"

export function Hero() {
  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-purple-600 via-pink-600 to-red-600">
      <div className="absolute inset-0 bg-black/20" />
      
      <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl md:text-6xl">
            <span className="block">樱花动漫</span>
            <span className="block text-purple-200">每周更新追踪</span>
          </h1>
          
          <p className="mx-auto mt-6 max-w-md text-xl text-purple-100 sm:max-w-3xl">
            实时追踪最新动漫更新，不错过任何一集精彩内容
          </p>
          
          <div className="mt-10 flex flex-col items-center justify-center space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
            <motion.a
              href="#weekly-updates"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="inline-flex items-center rounded-full bg-white px-8 py-3 text-base font-medium text-purple-600 shadow-lg transition-colors hover:bg-purple-50"
            >
              <Play className="mr-2 h-5 w-5" />
              开始浏览
            </motion.a>
            
            <motion.a
              href="#trending"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="inline-flex items-center rounded-full border border-white/30 bg-white/10 px-8 py-3 text-base font-medium text-white backdrop-blur-sm transition-colors hover:bg-white/20"
            >
              <TrendingUp className="mr-2 h-5 w-5" />
              热门推荐
            </motion.a>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3"
        >
          <div className="text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-white/20 backdrop-blur-sm">
              <Calendar className="h-8 w-8 text-white" />
            </div>
            <h3 className="mt-4 text-lg font-medium text-white">每日更新</h3>
            <p className="mt-2 text-sm text-purple-200">周一到周日，实时追踪</p>
          </div>
          
          <div className="text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-white/20 backdrop-blur-sm">
              <Star className="h-8 w-8 text-white" />
            </div>
            <h3 className="mt-4 text-lg font-medium text-white">高清画质</h3>
            <p className="mt-2 text-sm text-purple-200">1080P/4K 超清体验</p>
          </div>
          
          <div className="text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-white/20 backdrop-blur-sm">
              <TrendingUp className="h-8 w-8 text-white" />
            </div>
            <h3 className="mt-4 text-lg font-medium text-white">热门推荐</h3>
            <p className="mt-2 text-sm text-purple-200">精选人气动漫</p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}