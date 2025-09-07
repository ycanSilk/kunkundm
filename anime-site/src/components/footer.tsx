"use client"

import * as React from "react"

interface FooterProps {
  className?: string
  showCopyright?: boolean
  customText?: string
}

export function Footer({ 
  className, 
  showCopyright = true, 
  customText 
}: FooterProps) {
  return (
    <footer className={`bg-gray-900 text-white ${className || ''}`}>
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="text-center">
          <h3 className="text-lg font-semibold">樱花动漫追踪器</h3>
          <p className="mt-2 text-gray-400">
            {customText || "实时追踪最新动漫更新，不错过任何精彩内容"}
          </p>
          {showCopyright && (
            <p className="mt-4 text-sm text-gray-500">
              © 2025 樱花动漫追踪器. 仅供学习使用
            </p>
          )}
        </div>
      </div>
    </footer>
  )
}