#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樱花动漫广告移除测试脚本
针对你提供的具体URL: http://www.iyinghua.com/v/6543-1.html
和广告格式进行专门测试
"""

import sys
import os
from  import CleanVideoExtractor


def test_ad_removal():
    """测试广告移除功能"""
    
    # 你提供的具体URL
    test_url = "http://www.iyinghua.com/v/6543-1.html"
    
    print("🎯 樱花动漫广告移除测试")
    print("=" * 60)
    print(f"📺 测试URL: {test_url}")
    print("🎯 针对广告格式: <div id='adv_wrap_hh'>...</div>")
    print("🎯 广告域名: evewan.com, sogowan.com")
    print("=" * 60)
    
    # 创建提取器
    extractor = CleanVideoExtractor(headless=False)  # 设置为可见模式便于调试
    
    print("\n🔍 开始无广告提取...")
    
    # 执行提取
    result = extractor.extract_pure_m3u8(test_url)
    
    if result['success']:
        print("\n" + "="*70)
        print("✅ 广告移除成功！")
        print("="*70)
        
        if result['pure_m3u8']:
            print(f"🎬 找到 {len(result['pure_m3u8'])} 个无广告视频链接:")
            
            for i, link in enumerate(result['pure_m3u8'], 1):
                print(f"\n{i}. 📺 纯净视频链接:")
                print(f"   URL: {link['url']}")
                print(f"   类型: {link['type']}")
                print(f"   质量: {link['quality']}")
                print(f"   来源: {link['source']}")
                
                if link.get('valid'):
                    print("   ✅ 链接有效")
                else:
                    print("   ⚠️  链接需要验证")
        
        # 测试直接构造法
        print("\n" + "-"*50)
        print("🔧 测试直接构造法...")
        direct_result = extractor.construct_direct_url(test_url)
        
        if direct_result['success']:
            print(f"✅ 直接构造成功:")
            print(f"   🎯 纯净m3u8: {direct_result['direct_url']}")
            print(f"   📺 动漫ID: {direct_result['anime_id']}")
            print(f"   🔢 集数: {direct_result['episode']}")
        else:
            print(f"⚠️  直接构造失败: {direct_result['error']}")
    
    else:
        print("\n" + "="*70)
        print("❌ 广告移除失败")
        print("="*70)
        print(f"错误信息: {result['error']}")
        
        # 提供手动解决方案
        print("\n🔧 手动解决方案:")
        print("1. 使用你提供的原始m3u8链接")
        print("2. 手动清理广告参数")
        print("3. 使用ffmpeg直接下载")
    
    # 提供下载命令
    print("\n" + "="*50)
    print("📥 下载命令示例:")
    print("="*50)
    
    # 基于你提供的格式生成下载命令
    clean_url = "https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第01集/index.m3u8"
    
    print(f"🎬 纯净视频下载:")
    print(f"   ffmpeg -i \"{clean_url}\" -c copy -bsf:a aac_adtstoasc \"SilentWitch_第01集_无广告.mp4\"")
    
    print(f"\n📋 批量下载脚本:")
    print("""   # 批量下载所有集数
   for i in {01..12}; do
       url="https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第${i}集/index.m3u8"
       ffmpeg -i "$url" -c copy -bsf:a aac_adtstoasc "SilentWitch_第${i}集.mp4"
   done
    """)


if __name__ == "__main__":
    test_ad_removal()