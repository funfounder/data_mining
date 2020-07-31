import scrapy
from scrapy.http import Response
from pymongo import MongoClient

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['www.avito.ru']
    start_urls = ['https://www.avito.ru/kurskaya_oblast/nedvizhimost',
                  'https://www.avito.ru/kurskaya_oblast/kvartiry/prodam-ASgBAgICAUSSA8YQ']
    xpath_query = {
        'menu_links': '//li[contains(@class, "rubricator-list-item-item-tP77G")]//a/@href',
        'ads_items': '//div[contains(@class, "item__line")]//h3//a[contains(@class, "snippet-link"]',
    }

    data_base = MongoClient()

    def parse(self, response: Response):
        for link in response.xpath(self.xpath_query('menu_links')):
            yield response.follow(link, callback=self.ads_feed_parse)

    def ads_feed_parse(self, response: Response):
        for link in response.xpath(self.xpath_query('ads_item')):
            yield response.follow(link, callback=self.ads_item_parse)

    def ads_item_parse(self, response: Response):
        title = response.xpath('//h1/span[@itemprop="name"]/text()').extract_first()
        price = response.xpath('//span[@itemprop="rpice"]/@content').extract_first()
        yield {'title': title, 'price': price}

#    def save_to_mongo(self):
#        db = self.data_base['avito_gd']
#        collection = db['avito_nedviga']
#        pass