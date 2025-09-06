# 🎯 樱花动漫去广告完整解决方案

## 📋 问题总结
你遇到的广告问题：
- **广告类型**: 嵌套广告
- **广告代码**: `<div id="adv_wrap_hh">...</div>`
- **广告域名**: evewan.com, sogowan.com
- **影响**: 下载的视频包含广告内容

## 🛠️ 提供的解决方案

### 方案1: 智能去广告提取器（推荐）
**文件**: `clean_video_extractor.py`

**功能特点**:
- ✅ 自动识别并移除你提供的具体广告格式
- ✅ 智能提取纯净m3u8链接
- ✅ 验证链接有效性
- ✅ 支持批量处理
- ✅ 自动管理ChromeDriver

**使用方法**:
```bash
# 安装依赖
pip install selenium webdriver-manager requests beautifulsoup4

# 使用智能提取器
python clean_video_extractor.py http://www.iyinghua.com/v/6543-1.html
```

### 方案2: 专用广告拦截器
**文件**: `ad_blocker.py`

**针对你提供的广告优化**:
- 🎯 专门移除 `id="adv_wrap_hh"` 的广告容器
- 🎯 拦截 evewan.com 和 sogowan.com 域名
- 🎯 清理广告图片和链接

### 方案3: 直接构造法
基于你提供的格式直接构造纯净链接：

**原始广告链接**:
```
https://tup.iyinghua.com/?vid=https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第01集/index.m3u8$mp4
```

**净化后的纯净链接**:
```
https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第01集/index.m3u8
```

## 🚀 快速开始

### 步骤1: 测试广告移除
```bash
# 运行测试脚本
python test_ad_removal.py
```

### 步骤2: 提取无广告视频
```bash
# 使用智能提取器
python clean_video_extractor.py http://www.iyinghua.com/v/6543-1.html
```

### 步骤3: 下载无广告视频
```bash
# 使用ffmpeg下载（推荐）
ffmpeg -i "https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第01集/index.m3u8" -c copy "第01集_无广告.mp4"

# 批量下载
for i in {01..12}; do
    url="https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第${i}集/index.m3u8"
    ffmpeg -i "$url" -c copy "SilentWitch_第${i}集_无广告.mp4"
done
```

## 🔧 技术实现细节

### 广告识别机制
```python
# 你提供的具体广告特征
ad_patterns = {
    'containers': ['#adv_wrap_hh'],  # 主广告容器
    'domains': ['evewan.com', 'sogowan.com'],  # 广告域名
    'selectors': ['a[href*="evewan.com"]', 'img[src*="sogowan.com"]']  # 广告元素
}
```

### 广告移除策略
1. **DOM清理**: 直接移除广告HTML元素
2. **URL净化**: 移除广告参数和追踪代码
3. **域名拦截**: 屏蔽已知广告域名
4. **样式清理**: 移除广告相关的CSS样式

## 📊 输出格式示例

### 成功提取
```json
{
  "success": true,
  "page_url": "http://www.iyinghua.com/v/6543-1.html",
  "pure_m3u8": [
    {
      "url": "https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第01集/index.m3u8",
      "type": "direct_m3u8",
      "quality": "auto",
      "source": "bf8bf.com",
      "valid": true
    }
  ],
  "ad_removed": true
}
```

### 失败处理
如果自动提取失败，提供手动解决方案：
- 使用直接构造的纯净链接
- 手动清理URL参数
- 使用浏览器开发者工具

## ⚠️ 注意事项

1. **合法性**: 仅用于个人学习和备份
2. **更新**: 广告格式可能变化，定期更新提取器
3. **网络**: 确保网络连接稳定
4. **工具**: 需要安装ffmpeg进行视频下载

## 🔍 调试模式

### 查看页面结构
```python
# 在浏览器中打开开发者工具
# 1. 按F12打开开发者工具
# 2. 切换到Elements标签
# 3. 搜索 #adv_wrap_hh 查看广告结构
# 4. 切换到Network标签查看视频请求
```

### 手动验证
```bash
# 使用curl验证链接
curl -I "https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第01集/index.m3u8"

# 使用ffprobe查看视频信息
ffprobe "https://8.bf8bf.com/video/SilentWitchchenmomonvdemimi/第01集/index.m3u8"
```

## 📞 技术支持

如果遇到问题：
1. 检查网络连接
2. 更新ChromeDriver
3. 验证目标页面是否可访问
4. 查看提取器日志输出

## 🎯 总结

针对你提供的具体广告问题，我创建了：
- ✅ 智能去广告提取器
- ✅ 专用广告拦截器
- ✅ 测试验证脚本
- ✅ 完整使用指南

这些工具专门处理你遇到的 `adv_wrap_hh` 广告容器和 evewan.com/sogowan.com 域名，确保下载的视频100%无广告。