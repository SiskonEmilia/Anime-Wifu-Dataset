# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DatasetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GameInfo(scrapy.Item):
    name    = scrapy.Field()

class FaceItem(scrapy.Item):
    name       = scrapy.Field()
    image_urls = scrapy.Field()
    images     = scrapy.Field()