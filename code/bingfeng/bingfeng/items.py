# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BingfengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    board = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    floor = scrapy.Field()
    content = scrapy.Field()
    href = scrapy.Field()
    GmtDate = scrapy.Field()
    ViewCount = scrapy.Field()
    ResCount = scrapy.Field()
