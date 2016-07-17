# -*- coding: utf-8 -*-
import scrapy
from paidai.items import PaidaiItem
from scrapy.selector import Selector
import time
import re

baseUrl='http://bbs.paidai.com/v/topic-'
minIndex=2
maxIndex=4
urlList=[]
for i in range(minIndex,maxIndex+1):
    urlList.append(baseUrl+str(i))

class PdSpider(scrapy.Spider):
    global urlList
    name = "pd"
    allowed_domains = ["paidai.com"]
    start_urls = urlList

    def parse(self, response):
        global stopFlag
        sel = Selector(response)
        for lineSel in sel.xpath('//div[@class="content-bottom-l-2-m2"]/ul/li'):
            urlPage=lineSel.xpath('div/h4/a/@href').extract()[0]
            request = scrapy.Request(urlPage,callback=self.parse_info)
            yield request

    def parse_info(self,response):
        global stopFlag
        item = PaidaiItem()
        inSel = Selector(response)
        item['url']=response.url
        item['title']=inSel.xpath('//div[@id="t_title_info"]/h1[@class="t_title"]/text()').extract()[0]
        item['author']=inSel.xpath('//div[@id="t_title_info"]/p[@class="t_info"]/span[1]/a/text()').extract()[0]
        timeInfo=inSel.xpath('//div[@id="t_title_info"]/p[@class="t_info"]/span[2]/text()').extract()[0]
        #format time info
        #item['time']=formatTime(timeInfo)
        item['time']=timeInfo
        contents=inSel.xpath('//div[@id="topic_content"]').extract()[0]
        contents2=re.sub('<(.*?)>','',contents)
        item['contents']=re.sub('\s','',contents2)
        item['board']=u'找淘宝客'
        return item

    #format time info
    def formatTime(timeInfo):
        #if (timeInfo.find(':') == -1):
        pass


        
