'use client';

import React, { useEffect, useRef } from 'react';
import Artplayer from 'artplayer';
import '@/app/styles/artplayer.css';

interface ArtPlayerProps {
  url: string;
  title?: string;
  poster?: string;
  className?: string;
  onReady?: (player: Artplayer) => void;
  onPlay?: () => void;
  onPause?: () => void;
  onEnded?: () => void;
  onPrev?: () => void;
  onNext?: () => void;
  hasPrev?: boolean;
  hasNext?: boolean;
}

export default function ArtPlayer({
  url,
  title,
  poster,
  className = '',
  onReady,
  onPlay,
  onPause,
  onEnded,
  onPrev,
  onNext,
  hasPrev = true,
  hasNext = true,
}: ArtPlayerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const playerRef = useRef<Artplayer | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // 调试输出：开始创建播放器
    console.group('🎮 ArtPlayer 初始化');
    console.log('📺 播放URL:', url);
    console.log('🎬 视频标题:', title);
    console.groupEnd();

    // 创建ArtPlayer实例
    const art = new Artplayer({
      container: containerRef.current,
      url: url,
      title: title || '',
      poster: poster || '',
      volume: 0.5,
      isLive: false,
      muted: false,
      autoplay: false,
      pip: true, // 画中画
      autoSize: true,
      autoMini: true,
      screenshot: false, // 禁用截图
      setting: false, // 禁用设置
      loop: false,
      flip: true, // 翻转
      playbackRate: true, // 播放速度
      aspectRatio: true, // 宽高比
      fullscreen: true, // 全屏
      fullscreenWeb: true, // 网页全屏
      subtitleOffset: true, // 字幕偏移
      miniProgressBar: true, // 迷你进度条
      playsInline: true,
      layers: [],
      settings: [], // 清空设置选项
      controls: [
        {
          name: 'prev',
          index: 10,
          position: 'left',
          html: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><polygon points="15,18 9,12 15,6" /></svg>',
          tooltip: '上一集',
          style: {
            opacity: hasPrev ? 1 : 0.3,
            cursor: hasPrev ? 'pointer' : 'not-allowed',
            width: '44px',
            height: '44px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 2px 0 0'
          }
        },
        {
          name: 'next',
          index: 12,
          position: 'left',
          html: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><polygon points="9,6 15,12 9,18" /></svg>',
          tooltip: '下一集',
          style: {
            opacity: hasNext ? 1 : 0.3,
            cursor: hasNext ? 'pointer' : 'not-allowed',
            width: '44px',
            height: '44px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 0 0 2px'
          }
        },
      ],
      plugins: [], // 禁用所有插件（包括弹幕）
      theme: '#ff6b6b',
      lang: 'zh-cn',
      moreVideoAttr: {
        crossOrigin: 'anonymous',
      },
      customType: {
        m3u8: function playM3u8(video, url, art) {
          console.group('🎞️ HLS播放调试');
          console.log('🎯 HLS URL:', url);
          console.groupEnd();
          
          if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource(url);
            hls.attachMedia(video);
          } else {
            art.notice.show = '不支持播放格式';
          }
        },
      },
    });

    // 事件监听
    art.on('ready', () => {
      console.group('✅ ArtPlayer 就绪');
      console.log('🎬 播放器已准备就绪');
      console.log('📺 当前播放URL:', url);
      console.groupEnd();
      onReady?.(art);
    });

    art.on('play', () => {
      console.group('▶️ 开始播放');
      console.log('🎬 正在播放:', title);
      console.log('📺 播放URL:', url);
      console.groupEnd();
      onPlay?.();
    });

    art.on('pause', () => {
      console.group('⏸️ 暂停播放');
      console.log('🎬 已暂停:', title);
      console.groupEnd();
      onPause?.();
    });

    art.on('ended', () => {
      console.group('🛑 播放结束');
      console.log('🎬 播放完成:', title);
      console.groupEnd();
      onEnded?.();
    });

    art.on('control:prev', () => {
      console.group('⏮️ 上一集');
      console.log('🔄 切换到上一集');
      console.groupEnd();
      if (hasPrev && onPrev) {
        onPrev();
      }
    });

    art.on('control:next', () => {
      console.group('⏭️ 下一集');
      console.log('🔄 切换到下一集');
      console.groupEnd();
      if (hasNext && onNext) {
        onNext();
      }
    });

    // 保存播放器实例
    playerRef.current = art;

    // 清理函数
    return () => {
      if (playerRef.current) {
        playerRef.current.destroy();
        playerRef.current = null;
      }
    };
  }, [url, title, poster, onReady, onPlay, onPause, onEnded]);

  return (
    <div 
      ref={containerRef} 
      className={`artplayer-container ${className}`}
      style={{
        width: '100%',
        height: '100%',
        aspectRatio: '16/9',
      }}
    />
  );
}