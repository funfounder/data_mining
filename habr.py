from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from habr import settings
from habr.spiders.habr_parse import HabrParseSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_process = CrawlerProcess(settings=crawl_settings)
    crawl_process.crawl(HabrParseSpider)
    crawl_process.start()