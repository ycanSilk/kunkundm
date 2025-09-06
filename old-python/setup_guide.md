# 🌸 樱花动漫无广告播放器完整安装指南

## 📋 系统要求
- Python 3.7+
- Chrome浏览器
- 网络连接

## 🚀 快速安装

### 步骤1: 安装依赖
```bash
# 安装Python依赖
pip install flask flask-cors selenium webdriver-manager requests beautifulsoup4

# 如果pip版本过旧，先升级
pip install --upgrade pip
```

### 步骤2: 启动服务器
```bash
# 启动后端API服务器
python server.py
```

### 步骤3: 打开播放器
1. 打开浏览器
2. 访问 `web_player.html` 文件（直接双击即可）
3. 或者访问 `http://localhost:5000`

## 🎯 使用方法

### 基本使用
1. **输入URL**: 在输入框中粘贴樱花动漫页面URL
   - 示例: `http://www.iyinghua.com/v/6543-1.html`
   - 示例: `http://m.iyinghua.com/v/6543-1.html`

2. **点击播放**: 点击"解析并播放"按钮

3. **观看无广告视频**: 系统将自动解析并播放无广告视频

### 播放器功能
- ⏯️ **播放/暂停**: 空格键或播放按钮
- ⏮️ **上一集**: 上一集按钮
- ⏭️ **下一集**: 下一集按钮
- 🎚️ **播放速度**: 0.5x - 2x 可调
- ⌨️ **快捷键**:
  - 空格键: 播放/暂停
  - 左右箭头: 快进/快退10秒
  - 上下箭头: 音量调节

## 🔧 高级配置

### 自定义端口
```bash
# 修改server.py最后一行
app.run(host='0.0.0.0', port=8080, debug=True)
```

### 调试模式
```bash
# 启动调试模式
python server.py
# 查看控制台输出获取详细日志
```

## 📊 文件结构
```
yhdm/
├── server.py              # 后端API服务器
├── web_player.html        # 前端播放器界面
├── web_player.js          # 播放器核心逻辑
├── setup_guide.md         # 本安装指南
└── requirements.txt       # Python依赖列表
```

## 🛠️ 故障排除

### 常见问题

#### 1. ChromeDriver问题
```bash
# 错误信息: "chromedriver" executable needs to be in PATH
# 解决方案: webdriver-manager会自动下载，无需手动操作
```

#### 2. 端口占用
```bash
# 错误信息: Address already in use
# 解决方案: 修改server.py中的端口号
app.run(port=5001)  # 使用其他端口
```

#### 3. 跨域问题
```bash
# 错误信息: CORS policy error
# 解决方案: 已内置CORS支持，无需额外配置
```

#### 4. 视频无法播放
- **检查网络**: 确保网络连接正常
- **验证URL**: 确保樱花动漫URL有效
- **查看日志**: 检查server.py控制台输出

### 调试技巧

#### 查看详细日志
```bash
# 启动时添加详细日志
python server.py 2>&1 | tee debug.log
```

#### 浏览器开发者工具
1. 按F12打开开发者工具
2. 切换到Network标签查看API请求
3. 切换到Console标签查看JavaScript错误

## 🌐 网络要求
- 需要能够访问樱花动漫网站
- 需要能够下载m3u8视频文件
- 建议使用稳定网络连接

## 🔒 安全说明
- 本项目仅供学习和个人使用
- 请遵守当地法律法规
- 不要用于商业用途

## 📞 技术支持

### 获取帮助
1. **查看日志**: 运行server.py时的控制台输出
2. **检查URL**: 确保输入的樱花动漫URL格式正确
3. **网络测试**: 尝试在浏览器直接访问樱花动漫页面

### 手动测试
```bash
# 测试API
curl -X POST http://localhost:5000/api/parse \
  -H "Content-Type: application/json" \
  -d '{"url": "http://www.iyinghua.com/v/6543-1.html"}'

# 测试健康检查
curl http://localhost:5000/api/health
```

## 🎉 成功验证

当你看到以下信息时，表示安装成功：
```
🌸 启动樱花动漫解析服务器...
📍 访问 http://localhost:5000 查看API文档
📍 前端页面: web_player.html
```

## 📱 移动端使用
- 支持手机浏览器访问
- 响应式设计，自动适配屏幕
- 支持触摸手势控制

## 🚀 一键启动脚本

创建 `start.bat` (Windows):
```batch
@echo off
echo 🌸 启动樱花动漫无广告播放器...
python server.py
pause
```

创建 `start.sh` (Linux/Mac):
```bash
#!/bin/bash
echo "🌸 启动樱花动漫无广告播放器..."
python server.py
```

然后双击即可启动！