@echo off
title 🌸 樱花动漫无广告播放器
color 0A
echo.
echo    ╭────────────────────────────────────────╮
echo    │         🌸 樱花动漫无广告播放器        │
echo    │                                        │
echo    │  智能解析 · 实时去广告 · 高清播放      │
echo    ╰────────────────────────────────────────╯
echo.
echo 📦 正在检查依赖...
python -c "import flask" 2>nul || (
    echo ❌ 检测到缺少依赖，正在安装...
    pip install -r requirements.txt
)
echo.
echo 🚀 启动服务器...
python server.py
pause