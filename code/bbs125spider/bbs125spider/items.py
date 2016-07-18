# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Bbs125SpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # title, author, time, url, contents, board
    title = Field()
    author = Field()
    time = Field()
    url = Field()
    contents = Field()
    board = Field()