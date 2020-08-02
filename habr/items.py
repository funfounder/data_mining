# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def clean_images(value):
    if value[:2] == '//':
        return f'http:{value}'
    return value

def get_author_info(value):
    print(1)

class HabrItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    post_url = scrapy.Field()
    title = scrapy.Field()
    author_name = scrapy.Field()
    author_url = scrapy.Field()
    comments = scrapy.Field()
    iamges = scrapy.Field()

class HabrAuthorInfoItem(scrapy.Item):
    author_info = scrapy.Field(input_processor=MapCompose(get_author_info))




