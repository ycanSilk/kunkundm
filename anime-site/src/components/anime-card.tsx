"use client"

import * as React from "react"
import { motion } from "framer-motion"
import { Play, Star, Calendar } from "lucide-react"
import { Anime } from "@/types/anime"
import { cn, truncateText } from "@/lib/utils"

interface AnimeCardProps {
  anime: Anime
  className?: string
}

export function AnimeCard({ anime, className }: AnimeCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={cn("group relative overflow-hidden rounded-xl bg-white shadow-lg transition-all duration-300 hover:shadow-2xl", className)}
    >
      <div className="aspect-[3/4] overflow-hidden">
        <div className="h-full w-full bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
          <div className="flex h-full items-center justify-center">
            <div className="text-center text-white">
              <div className="text-4xl font-bold">{anime.episode}</div>
              <div className="text-sm opacity-80">{truncateText(anime.title, 15)}</div>
            </div>
          </div>
        </div>
        <div className="absolute inset-0 bg-black/60 opacity-0 transition-opacity duration-300 group-hover:opacity-100">
          <div className="flex h-full items-center justify-center">
            <Play className="h-12 w-12 text-white" />
          </div>
        </div>
      </div>
      
      <div className="p-4">
        <h3 className="text-lg font-bold text-gray-900 line-clamp-1">{anime.title}</h3>
        <p className="text-sm text-gray-600">{anime.episode}</p>
        
        <div className="mt-2 flex items-center justify-between">
          <div className="flex items-center space-x-1">
            <Star className="h-4 w-4 text-yellow-400 fill-current" />
            <span className="text-sm font-medium">{anime.rating}</span>
          </div>
          <div className="flex items-center space-x-1 text-gray-500">
            <Calendar className="h-3 w-3" />
            <span className="text-xs">{anime.releaseDate}</span>
          </div>
        </div>
        
        <div className="mt-2 flex flex-wrap gap-1">
          {anime.genres.slice(0, 2).map((genre) => (
            <span
              key={genre}
              className="rounded-full bg-purple-100 px-2 py-1 text-xs font-medium text-purple-800"
            >
              {genre}
            </span>
          ))}
        </div>
      </div>
      
      <a
        href={anime.url}
        target="_blank"
        rel="noopener noreferrer"
        className="absolute inset-0"
      />
    </motion.div>
  )
}