"""
爬虫配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:3000')
API_ENDPOINT = f"{API_BASE_URL}/api/crawler"

# 爬虫配置
CRAWLER_CONFIG = {
    # 请求延迟
    'REQUEST_DELAY': 1.0,
    
    # 重试配置
    'MAX_RETRIES': 3,
    'RETRY_DELAY': 2.0,
    
    # 超时配置
    'REQUEST_TIMEOUT': 10,
    
    # 用户代理
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # 并发限制
    'MAX_CONCURRENT': 5,
    
    # 缓存配置
    'CACHE_ENABLED': True,
    'CACHE_TTL': 3600  # 1小时
}

# 数据源配置
DATA_SOURCES = {
    'yhdm': {
        'base_url': 'https://www.yhdm.tv',
        'enabled': True,
        'rate_limit': 1.0
    },
    'agefans': {
        'base_url': 'https://www.agefans.cc',
        'enabled': True,
        'rate_limit': 1.5
    }
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'crawler.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}