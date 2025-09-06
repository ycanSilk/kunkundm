import { Hero } from "@/components/hero"
import { Navbar } from "@/components/navbar"
import { WeeklyUpdates } from "@/components/weekly-updates"
import { mockWeeklyUpdates } from "@/lib/mock-data"

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <Hero />
      
      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="space-y-12">
          <section id="weekly-updates" className="scroll-mt-20">
            <div className="mb-8 text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                每周更新列表
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                按周一到周日分类的最新动漫更新
              </p>
            </div>
            <WeeklyUpdates updates={mockWeeklyUpdates} />
          </section>

          <section id="trending" className="scroll-mt-20">
            <div className="mb-8 text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                热门推荐
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                本周最受欢迎的动漫作品
              </p>
            </div>
            
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {/* 这里可以添加热门推荐的卡片 */}
            </div>
          </section>
        </div>
      </main>

      <footer className="bg-gray-900 text-white">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-lg font-semibold">樱花动漫追踪器</h3>
            <p className="mt-2 text-gray-400">
              实时追踪最新动漫更新，不错过任何精彩内容
            </p>
            <p className="mt-4 text-sm text-gray-500">
              © 2025 樱花动漫追踪器. 仅供学习使用
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
