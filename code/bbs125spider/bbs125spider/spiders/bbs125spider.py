#-*-coding:utf8-*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector # use XPath
from bbs125spider.items import Bbs125spiderItem # this class include what items we want to get

class bbs125Spider(CrawlSpider): # Crawlspider is this class's father
    name = "bbs125spider"
    redis_key = 'bbs125spider:start_urls'
    start_urls = ['http://bbs.125.la/']
    # start_urls = ['http://www.tianya88.com/']

    def parse(self, response):
        selector = Selector(response) # get the source code of web page
        table = selector.xpath('//table')
        for each in table:
            bookName = each.xpath('tr/td[@colspan="3"]/center/h2/text()').extract()[0]
            content = each.xpath('tr/td/a/text()').extract()
            url = each.xpath('tr/td/a/@href').extract()
            for i in range(len(url)):
                item = NovelspiderItem()
                item['bookName'] = bookName
                item['chapterURL'] = url[i]
                try:
                    item['bookTitle'] = content[i].split(' ')[0]
                    item['chapterNum'] = content[i].split(' ')[1]
                except Exception, e:
                    continue

                try:
                    item['chapterName'] = content[i].split(' ')[2]
                except Exception, e:
                    item['chapterName'] = content[i].split(' ')[1][-3:]
                yield item
