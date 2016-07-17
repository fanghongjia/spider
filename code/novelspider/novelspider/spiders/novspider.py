#-*-coding:utf8-*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector # use XPath
from novelspider.items import NovelspiderItem # this class include what items we want to get

class novSpider(CrawlSpider): # Crawlspider is this class's father
    name = "novspider"
    redis_key = 'nvospider:start_urls'
    start_urls = ['http://www.daomubiji.com/']

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
