import scrapy
from scrapy.http import Response
from scrapy.loader import ItemLoader
from pymongo import MongoClient

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['www.avito.ru']
    start_urls = ['https://www.avito.ru/kurskaya_oblast/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1'
                  ]

    xpath_query = {
        'menu_links': '//li[contains(@class, "rubricator-list-item-item-tP77G")]//a/@href',
        'ads_items': '//div[contains(@class, "item__line")]//h3//a[contains(@class, "snippet-link")]',
        'pagination_links': '//div[contains(@class, "pagination-pages.clearfix")]//a[contains(@class, "pagination-page")]',
        'item_params': '//div[contains(@class, "item-params")]/ul[contains(@class, "item-params-list")]',
        'single_param': '//div[contains(@class, "item-params")]/span[contains(@class, "item-params-label")]'
    }

    data_base_client = MongoClient()
    avito_nedviga = []

    def parse(self, response: Response):
        for link in response.xpath(self.xpath_query['menu_links']):
            yield response.follow(link, callback=self.ads_feed_parse)

    def ads_feed_parse(self, response: Response):
        for link in response.xpath(self.xpath_query['ads_items']):
            yield response.follow(link, callback=self.ads_item_parse)

    def ads_item_parse(self, response: Response):
        title = response.xpath('//h1/span[@itemprop="name"]/text()').extract_first()
        url = response.url
        price = response.xpath('//span[@itemprop="price"]/@content').extract_first()
        parameters = []
        if response.xpath(self.xpath_query['item_params']):
            for item in response.xpath(self.xpath_query['item_params']):
                parameters.extend(item.xpath('//li[contains(@class, "item-params-list-item"]/span[contains(@class, "item-params-label")]').extract())
        elif response.xpath(self.xpath_query['single_param']):
            key = response.xpath('//div[contains(@class, "item-params")]/span/span/text()[1]').extract_first()
            value = response.xpath('//div[contains(@class, "item-params")]/span/text()[2]').extract_first()
            parameters.append({key: value})
            # parameters.extend(response.xpath(self.xpath_query['single_param']).extract())
        yield self.avito_nedviga.append({'title': title, 'price': price, 'url': url, 'params': parameters})

    def pagination_parse(self, response: Response):
        for link in response.xpath(self.xpath_query['pagination_links']):
            yield response.follow(link, callback=self.ads_feed_parse)

    def save_to_mongo(self):
        db = self.data_base_client['avito_db']
        collection = db['avito_nedviga']
        collection.insert_many(self.avito_nedviga)