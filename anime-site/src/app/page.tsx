import { Header } from "@/components/header"
import { Footer } from "@/components/footer"

import { DailyAnimeSidebar } from "@/components/daily-anime-sidebar"
import { LatestAnimeGrid } from "@/components/latest-anime-grid"
import Link from "next/link"
import HomeSearch from "@/components/home-search"
import fs from 'fs'
import path from 'path'

export default async function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <HomeSearch />
      
      <main className="container mx-auto max-w-7xl px-3 py-6 sm:px-4 sm:py-8 lg:px-6 lg:py-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6 lg:gap-8">
          {/* 左边 - 最新更新 */}
          <div className="col-span-1 lg:col-span-8">
            <section id="recommendations" className="scroll-mt-20">
              <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-gray-900 mb-4 sm:mb-5">
                  最新更新
              </h2>
              <LatestAnimeGrid />
            </section>
          </div>

          {/* 右边 - 每日更新 */}
          <div className="col-span-1 lg:col-span-4">
            <DailyAnimeSidebar />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
