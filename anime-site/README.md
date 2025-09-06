# 樱花动漫追踪器 🌸

一个使用React + Next.js + TypeScript + Tailwind CSS构建的现代动漫追踪网站。

## 🚀 项目特点

- **现代化技术栈**: 使用Next.js 15、React 19、TypeScript和Tailwind CSS
- **响应式设计**: 完美适配桌面端和移动端
- **动画效果**: 使用Framer Motion实现流畅的交互动画
- **组件化架构**: 清晰的组件分离和可复用设计
- **实时数据**: 集成樱花动漫网站的每周更新数据

## ✨ 功能特性

### 已完成功能
- ✅ 现代化首页设计
- ✅ 响应式导航栏
- ✅ 英雄区域展示
- ✅ 每周更新列表（按周一到周日分类）
- ✅ 动漫卡片展示
- ✅ 搜索功能（界面）
- ✅ 移动端适配

### 数据结构
- **动漫信息**: 包含标题、集数、描述、评分、发布日期等
- **每周更新**: 按周一到周日分类的更新列表
- **热门推荐**: 精选热门动漫作品

## 🏗️ 项目结构

```
anime-site/
├── src/
│   ├── app/
│   │   ├── globals.css          # 全局样式
│   │   ├── layout.tsx          # 根布局
│   │   └── page.tsx            # 首页
│   ├── components/
│   │   ├── anime-card.tsx      # 动漫卡片组件
│   │   ├── hero.tsx            # 英雄区域组件
│   │   ├── navbar.tsx          # 导航栏组件
│   │   ├── weekly-updates.tsx  # 每周更新组件
│   │   └── ui/
│   │       └── card.tsx        # 基础卡片组件
│   ├── lib/
│   │   ├── mock-data.ts        # 模拟数据
│   │   └── utils.ts            # 工具函数
│   └── types/
│       └── anime.ts            # TypeScript类型定义
├── package.json
├── tailwind.config.ts          # Tailwind配置
└── tsconfig.json               # TypeScript配置
```

## 🚦 安装和运行

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

访问 http://localhost:3000 查看网站。

### 构建生产版本
```bash
npm run build
npm start
```

## 📊 数据来源

本项目使用模拟数据展示动漫更新信息。在实际应用中，可以通过以下方式获取数据：

1. **API集成**: 集成第三方动漫API
2. **爬虫数据**: 使用Node.js爬虫定期抓取更新
3. **用户提交**: 允许用户提交更新信息

## 🛠️ 技术栈

- **前端框架**: Next.js 15 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **动画**: Framer Motion
- **图标**: Lucide React
- **工具函数**: clsx, tailwind-merge

## 🌐 浏览器支持

- Chrome (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- Edge (最新版本)

## 📋 开发计划

- [ ] 添加搜索功能
- [ ] 实现用户收藏
- [ ] 添加动漫详情页面
- [ ] 集成真实API数据
- [ ] 添加用户登录系统
- [ ] 实现推送通知
- [ ] 添加评论系统

## 📄 许可证

仅供学习使用，请勿用于商业用途。
