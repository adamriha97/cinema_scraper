from cinema_scraper_project.spiders.cinestar_program_spider import CinestarProgramSpiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def crawl_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(CinestarProgramSpiderSpider)
    process.start()


crawl_spiders()