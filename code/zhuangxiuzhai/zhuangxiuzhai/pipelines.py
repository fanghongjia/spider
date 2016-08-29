# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo

class ZhuangxiuzhaiPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        client.admin.authenticate(settings['MONGODB_USER'], settings['MONGODB_PSW'])
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        postInfo = dict(item)
        self.post.insert(postInfo)
        return item

    # when spider opened, this method workhref
    def open_spider(self, spider):
        print 'spider begin to crawl!'

    # when spider closed, this method work, may we can send email in this def
    def close_spider(self, spider):
        print 'spider closed!'
