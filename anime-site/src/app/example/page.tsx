import { Header } from "@/components/header"
import { Footer } from "@/components/footer"

export default function ExamplePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* 使用自定义配置的Header（导航栏） */}
      <Header />
      
      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            组件复用示例页面
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            这个页面展示了Header（导航栏）、Hero（英雄区域）和Footer组件的复用性
          </p>
          
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-semibold mb-4">组件特性</h2>
            <ul className="text-left space-y-2 text-gray-700">
              <li>✅ Header组件（导航栏）支持自定义导航项和搜索框</li>
              <li>✅ Hero组件支持自定义className和样式</li>
              <li>✅ Footer组件支持自定义文本和版权显示</li>
              <li>✅ 完全响应式设计</li>
              <li>✅ 流畅的动画效果</li>
              <li>✅ TypeScript类型安全</li>
            </ul>
          </div>
        </div>
      </main>
      
      {/* 使用自定义配置的Footer */}
      <Footer 
        customText="这是示例页面的自定义页脚文本"
        showCopyright={true}
        className="mt-16"
      />
    </div>
  )
}