# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo

class Www52FzbaPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        client.admin.authenticate(settings['MONGODB_USER'], settings['MONGODB_PSW'])
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        item_dict = dict(item)
        # 以下两行为了使除一楼外其他楼层不存储url
        item_pop_herf = item_dict.copy()
        item_pop_herf.pop('href')
        if item_dict.has_key('title'):
            postInfo = {'1': item_dict}
            self.post.insert(postInfo)
        else:
            fields = len(self.post.find_one({"1.href": item_dict['href']}))
            item_pop_herf['floor'] = str(fields)
            postInfo = {str(fields): item_pop_herf}
            self.post.update({"1.href": item_dict['href']}, {"$set": postInfo})
        return item

        # when spider opened, this method workhref

    def open_spider(self, spider):
        print 'spider begin to crawl!'

        # when spider closed, this method work, may we can send email in this def

    def close_spider(self, spider):
        print 'spider closed!'