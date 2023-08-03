# Scrapy settings for bid_scrapy_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import time

BOT_NAME = "bid_scrapy_project"

SPIDER_MODULES = ["bid_scrapy_project.spiders", "bid_scrapy_project.spiders_1"]
NEWSPIDER_MODULE = "bid_scrapy_project.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'bid_scrapy_project (+http://www.yourdomain.com)'
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 配置日志,线上开启
# LOG_LEVEL = "ERROR"
LOG_LEVEL = "INFO"
# LOG_LEVEL = "DEBUG"
# nowTime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
# LOG_PATH = f"./logs/{nowTime}"
# if not os.path.exists(LOG_PATH):
#     os.makedirs(LOG_PATH)
# LOG_FILE = "{}.log".format(LOG_PATH)


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4
# DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 20
# 超时自动关闭
CLOSESPIDER_TIMEOUT = 480
# 特殊类自动关闭配置
SPECIAL_CLOSESPIDER_TIMEOUT = 1000


# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'bid_scrapy_project.middlewares.BidScrapyProjectSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'bid_scrapy_project.middlewares.BidScrapyProjectDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "bid_scrapy_project.pipelines.DupefilterPipeline": 288,  # 过滤列表页直取详情数据
    # "bid_scrapy_project.pipelines.BidScrapyProjectPipeline": 300,  # 线下测试使用,正式环境关闭
    # 'bid_scrapy_project.pipelines.KafkaPipeline': 303, # kafka启动卡关,正式环境开启
    # 'crawlab.pipelines.CrawlabMongoPipeline': 888, # crawlab
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 线上mysql
# MYSQL_HOST = "10.67.78.131"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "121314"
# MYSQL_DBNAME = "bid_project"
# MYSQL_PORT = 3306
# MYSQL_TABLE_NAME = 't_zx_bid_crawl_info'
# MYSQL_TABLE_NAME_PROCURE = 't_zx_po_crawl_info'
# MYSQL_TABLE_NAME_NEW = 't_zx_bid_info'

# 线上
REDIS_HOST = "10.67.78.130"
REDIS_PORT = "6379"
REDIS_ENCODING = "utf-8"
REDIS_PWD = "qwer1234"
REDIS_PARAMS = {"db": 1, "password": REDIS_PWD}


# 本地redis
# REDIS_HOST = "127.0.0.1"
# REDIS_PWD = ""
# REDIS_PORT = "6379"
# REDIS_ENCODING = "utf-8"
# REDIS_PARAMS = {"db": 13, "password": REDIS_PWD}


# 本地mysql
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_PORT = 3306
MYSQL_DBNAME = "bid_project"
MYSQL_TABLE_NAME = "t_zx_bid_crawl_info"
MYSQL_TABLE_NAME_PROCURE = "t_zx_po_crawl_info"
MYSQL_TABLE_NAME_NEW = "t_zx_bid_info"


# 线上kafka相关配置
KAFKA_IP_PORT = ["10.67.78.132:9092"]
KAFKA_TOPIC_NAME = 'bid_info' # 线上使用，测试不要开启

# 本地kafka相关配置
# KAFKA_IP_PORT = ["127.0.0.1:9092"]
# KAFKA_TOPIC_NAME = "bid_scrapy"


# scrapy-redis 去重相关配置
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_QUEUE_KEY = "%(spider)s:requests"
SCHEDULER_DUPEFILTER_KEY = "%(spider)s:dupefilter"
SCHEDULER_PERSIST = True
