from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avito_parse import settings
from avito_parse.spiders.avito import AvitoSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_process = CrawlerProcess(settings=crawl_settings)
    crawl_process.crawl(AvitoSpider)
    crawl_process.start()
