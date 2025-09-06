// 樱花动漫无广告播放器核心脚本

class SakuraPlayer {
    constructor() {
        this.videoPlayer = document.getElementById('videoPlayer');
        this.currentUrl = '';
        this.currentEpisode = 1;
        this.totalEpisodes = 1;
        this.videoBaseUrl = '';
        this.isPlaying = false;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupSpeedControl();
        this.setupAdBlocker();
    }

    bindEvents() {
        // 视频事件
        this.videoPlayer.addEventListener('loadedmetadata', () => {
            this.showStatus('视频加载成功！正在移除广告...', 'success');
            this.removeAds();
        });

        this.videoPlayer.addEventListener('error', (e) => {
            this.showStatus('视频加载失败，请检查URL或网络连接', 'error');
            console.error('Video error:', e);
        });

        this.videoPlayer.addEventListener('ended', () => {
            this.playNext();
        });

        // 键盘快捷键
        document.addEventListener('keydown', (e) => {
            switch(e.code) {
                case 'Space':
                    e.preventDefault();
                    this.togglePlayPause();
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    this.videoPlayer.currentTime -= 10;
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    this.videoPlayer.currentTime += 10;
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.videoPlayer.volume = Math.min(1, this.videoPlayer.volume + 0.1);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.videoPlayer.volume = Math.max(0, this.videoPlayer.volume - 0.1);
                    break;
            }
        });
    }

    setupSpeedControl() {
        const speedSlider = document.getElementById('speedSlider');
        const speedDisplay = document.getElementById('speedDisplay');

        speedSlider.addEventListener('input', (e) => {
            const speed = parseFloat(e.target.value);
            this.videoPlayer.playbackRate = speed;
            speedDisplay.textContent = `${speed}x`;
        });
    }

    setupAdBlocker() {
        // 预处理广告过滤
        this.adBlocker = new AdBlocker();
        
        // 实时广告监控
        this.setupAdObserver();
    }

    setupAdObserver() {
        // 创建MutationObserver监控DOM变化
        this.observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // Element node
                        this.adBlocker.checkAndRemoveAd(node);
                    }
                });
            });
        });

        // 开始监控
        this.observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // 前端不再处理URL解析，完全依赖后端
    // 解析逻辑已移至parseAndPlay函数

    loadVideo(episode) {
        if (!this.videoBaseUrl) return;

        // 构造当前集数的视频URL
        const videoUrl = this.constructEpisodeUrl(episode);
        
        this.showStatus('正在加载视频...', 'info');
        
        // 添加错误处理和备用方案
        this.videoPlayer.onerror = (e) => {
            console.error('视频加载错误:', e);
            this.showStatus('视频加载失败，尝试备用方案...', 'error');
            
            // 使用备用测试视频
            this.videoPlayer.src = 'https://www.w3schools.com/html/mov_bbb.mp4';
            this.videoPlayer.load();
        };

        this.videoPlayer.onloadeddata = () => {
            this.hideLoading();
            this.showStatus('视频加载成功！', 'success');
        };

        this.videoPlayer.src = videoUrl;
        this.videoPlayer.load();
    }

    constructEpisodeUrl(episode) {
        // 根据视频URL模式构造当前集数URL
        let url = this.videoBaseUrl;
        
        // 如果是测试视频，直接返回
        if (url.includes('w3schools.com') || url.includes('sample-videos.com')) {
            return url;
        }
        
        // 处理不同格式的URL
        if (url.includes('第01集')) {
            url = url.replace('第01集', `第${episode.toString().padStart(2, '0')}集`);
        } else if (url.includes('EP01')) {
            url = url.replace('EP01', `EP${episode.toString().padStart(2, '0')}`);
        } else if (url.includes('episode=1')) {
            url = url.replace('episode=1', `episode=${episode}`);
        } else if (url.includes('01.mp4')) {
            url = url.replace('01.mp4', `${episode.toString().padStart(2, '0')}.mp4`);
        } else if (url.includes('/1/')) {
            url = url.replace('/1/', `/${episode}/`);
        }
        
        return url;
    }

    removeAds() {
        // 预处理广告过滤
        this.adBlocker.removeAllAds();
        
        // 实时广告过滤
        setInterval(() => {
            this.adBlocker.removeAllAds();
        }, 1000);
    }

    togglePlayPause() {
        if (this.videoPlayer.paused) {
            this.videoPlayer.play();
            this.isPlaying = true;
        } else {
            this.videoPlayer.pause();
            this.isPlaying = false;
        }
    }

    playPrevious() {
        if (this.currentEpisode > 1) {
            this.currentEpisode--;
            this.loadVideo(this.currentEpisode);
            this.updateEpisodeInfo();
        }
    }

    playNext() {
        if (this.currentEpisode < this.totalEpisodes) {
            this.currentEpisode++;
            this.loadVideo(this.currentEpisode);
            this.updateEpisodeInfo();
        }
    }

    updateEpisodeInfo() {
        document.getElementById('currentEpisode').textContent = `第 ${this.currentEpisode} 集`;
        document.getElementById('totalEpisodes').textContent = `/ 共 ${this.totalEpisodes} 集`;
    }

    showStatus(message, type) {
        const statusEl = document.getElementById('status');
        statusEl.textContent = message;
        statusEl.className = `status ${type}`;
        statusEl.classList.remove('hidden');
        
        setTimeout(() => {
            statusEl.classList.add('hidden');
        }, 5000);
    }

    showLoading() {
        document.getElementById('loading').classList.add('active');
        document.getElementById('playerContainer').classList.add('hidden');
    }

    hideLoading() {
        document.getElementById('loading').classList.remove('active');
        document.getElementById('playerContainer').classList.remove('hidden');
    }
}

class AdBlocker {
    constructor() {
        this.adSelectors = [
            '#adv_wrap_hh',
            'div[id*="adv"]',
            'div[class*="ad"]',
            'a[href*="evewan.com"]',
            'a[href*="sogowan.com"]',
            'img[src*="sogowan.com"]',
            'iframe[src*="visitor"]'
        ];
    }

    checkAndRemoveAd(element) {
        // 检查元素本身
        if (this.isAdElement(element)) {
            element.remove();
            return;
        }

        // 检查子元素
        const ads = element.querySelectorAll && element.querySelectorAll(this.adSelectors.join(','));
        if (ads) {
            ads.forEach(ad => ad.remove());
        }
    }

    isAdElement(element) {
        if (!element || !element.tagName) return false;

        const tagName = element.tagName.toLowerCase();
        
        // 检查ID
        if (element.id && (
            element.id.includes('adv') ||
            element.id.includes('ad')
        )) {
            return true;
        }

        // 检查类名
        if (element.className && (
            element.className.includes('ad') ||
            element.className.includes('banner')
        )) {
            return true;
        }

        // 检查链接
        if (tagName === 'a') {
            const href = element.getAttribute('href') || '';
            if (href.includes('evewan.com') || href.includes('sogowan.com')) {
                return true;
            }
        }

        // 检查图片
        if (tagName === 'img') {
            const src = element.getAttribute('src') || '';
            if (src.includes('sogowan.com') || src.includes('visitor')) {
                return true;
            }
        }

        // 检查样式
        const style = element.style;
        if (style && (
            style.zIndex === '10000000' ||
            (style.position === 'absolute' && style.width === '600px')
        )) {
            return true;
        }

        return false;
    }

    removeAllAds() {
        // 移除所有已知的广告元素
        this.adSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => el.remove());
        });

        // 移除特定样式的广告
        const styledAds = document.querySelectorAll('[style*="z-index: 10000000"]');
        styledAds.forEach(ad => ad.remove());

        // 移除绝对定位的广告
        const absoluteAds = document.querySelectorAll('[style*="position: absolute"]');
        absoluteAds.forEach(ad => {
            const style = ad.style;
            if (style.width === '600px' && style.height === '400px') {
                ad.remove();
            }
        });
    }
}

// 全局函数
let player;

function parseAndPlay() {
    const url = document.getElementById('videoUrl').value.trim();
    if (!url) {
        alert('请输入有效的樱花动漫URL');
        return;
    }

    if (!player) {
        player = new SakuraPlayer();
    }

    player.parseVideoUrl(url);
}

function clearUrl() {
    document.getElementById('videoUrl').value = '';
    if (player) {
        player.videoPlayer.src = '';
        document.getElementById('playerContainer').classList.add('hidden');
    }
}

function togglePlayPause() {
    if (player) {
        player.togglePlayPause();
    }
}

function playPrevious() {
    if (player) {
        player.playPrevious();
    }
}

function playNext() {
    if (player) {
        player.playNext();
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌸 樱花动漫无广告播放器已加载');
});

// 错误处理
window.addEventListener('error', (e) => {
    console.error('播放器错误:', e.error);
});

// 防止右键菜单（可选）
document.addEventListener('contextmenu', (e) => {
    if (e.target.tagName === 'VIDEO') {
        e.preventDefault();
    }
});