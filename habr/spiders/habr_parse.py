import scrapy
from scrapy.http import Response
from scrapy.loader import ItemLoader
from habr.items import HabrItem, HabrAuthorInfoItem
from pymongo import MongoClient


class HabrParseSpider(scrapy.Spider):
    name = 'habr_parse'
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/top/']

    xpath_query = {
        'post_link': '//h2[contains(@class, "post__title")]//a/@href',
        'ads_items': '//div[contains(@class, "item__line")]//h3//a[contains(@class, "snippet-link")]',
        'pagination_links': '//div[contains(@class, "pagination-pages.clearfix")]//a[contains(@class, "pagination-page")]',
        'item_params': '//div[contains(@class, "item-params")]/ul[contains(@class, "item-params-list")]',
        'single_param': '//div[contains(@class, "item-params")]/span[contains(@class, "item-params-label")]'
    }

    # data_base_client = MongoClient()
    # habr_posts = []

    def parse(self, response: Response):
        for link in response.xpath(self.xpath_query['post_link']):
            yield response.follow(link, callback=self.posts_parse)
 #           yield response.follow(link, callback=self.author_info)


    def posts_parse(self, response: Response):
        item = ItemLoader(HabrItem(), response)
        item.add_value('post_url', response.url)
        item.add_xpath('title', '//h1[contains(@class, "post__title.post__title_full")]/text()')
        item.add_xpath('author_name', '//header[contains(@class, "post__meta")]/a/span/text()')
        item.add_xpath('author_url','//header[contains(@class, "post__meta")]/a/@href')
        item.add_xpath('comments', '//h2[contains(@class, "comments-section__head-title")]/span[contains(@class, "comments-section__head-counter")]/text()')
        item.add_xpath('iamges', '//div[contains(@class, "post__body.post__body_full")]//p/img/@src')
        yield item.load_item()

    def author_info(self, response: Response):
        item = ItemLoader(HabrAuthorInfoItem(), response)
        item.add_xpath('author_info', '//div[contains(@class, "default-block__content.default-block__content_profile-summary")]/ul[contains(@class, "defination-list")]/li[contains(@class, "defination-list__item.defination-list__item_profile-summary")]')
        yield item.load_item()


# def save_to_mongo(self):
#     db = self.data_base_client['habr_db']
#     collection = db['habr_posts']
#     collection.insert_many(self.habr_posts)