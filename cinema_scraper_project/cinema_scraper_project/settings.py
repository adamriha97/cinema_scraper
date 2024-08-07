# Scrapy settings for cinema_scraper_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "cinema_scraper_project"

SPIDER_MODULES = ["cinema_scraper_project.spiders"]
NEWSPIDER_MODULE = "cinema_scraper_project.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "cinema_scraper_project (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "cinema_scraper_project.middlewares.CinemaScraperProjectSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    "cinema_scraper_project.middlewares.CinemaScraperProjectDownloaderMiddleware": 543,
    'cinema_scraper_project.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,
    'cinema_scraper_project.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 300,
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550, 
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None, 
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #"cinema_scraper_project.pipelines.CinemaScraperProjectPipeline": 300,
    #"cinema_scraper_project.pipelines.CinestarSpiderPipeline": 300,
    #"cinema_scraper_project.pipelines.MongoDBPipeline": 700
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"



# settings.py - for scrapy_playwright

#DOWNLOAD_HANDLERS = {
#    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#}

## settings.py - for scrapy_selenium

# for Chrome driver 
#from shutil import which
  
##SELENIUM_DRIVER_NAME = 'chrome'
#SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver.exe')
##SELENIUM_DRIVER_ARGUMENTS=['--headless'] # '--headless'
  
##DOWNLOADER_MIDDLEWARES = {
##     'scrapy_selenium.SeleniumMiddleware': 800
##     }


# Set other settings

import os
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

#with open('cinema_scraper_project\SCRAPEOPS_API_KEY.txt', 'r') as file:
#    SCRAPEOPS_API_KEY = file.read()
#SCRAPEOPS_API_KEY = '50b1fdde-ac43-48e8-af20-100564a98a0d'
SCRAPEOPS_API_KEY = os.environ["SCRAPEOPS_API_KEY"]
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5

MONGODB_URI = os.environ["MONGODB_URI"]
MONGODB_DATABASE = os.environ["MONGODB_DATABASE"]

DAYS_AHEAD_TO_SCRAPE = 14
YEARS_OF_PREMIERES = [datetime.now().year]