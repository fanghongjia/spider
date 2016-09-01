#-*-coding:utf8-*-

import sys
import time
import random
import scrapy
from scrapy.selector import Selector
from pediy.items import PediyItem  # 报错是pyCharm的原因

reload(sys)
sys.setdefaultencoding('utf-8')

class pediySpider(scrapy.spiders.Spider):
    name = "pediy"  # 在命令行中输入scrapy crawl bbs125启动此爬虫
    allowed_domains = ["pediy.com"]  # 非此域名的url不爬
    cookies = {
        "bbsessionhash": "0941fba1fd3c8c5b808f5d51ea4b7e8b",
        "bblastvisit": "1472530328",
        "bblastactivity": "0",
        "__jsluid": "bce55539323efbd30cb5abfbcbeaa651",
        "bbuserid": "729489",
        "bbpassword": "ae95077a901b516a4f21e87a9307277e",
        "__utma": "153457209.300808106.1472530520.1472530520.1472530520.1",
        "__utmb": "153457209.2.10.1472530520",
        "__utmc": "153457209",
        "__utmz": "153457209.1472530520.1.1.utmcsr=bbs.pediy.com|utmccn=(referral)|utmcmd=referral|utmcct=/forumdisplay.php",
        "bbforum_view": "55a0f7ac2ab1d983c076dffac66770ba240fdd20a-5-%7Bi-161_i-1472531033_i-45_i-1472530585_i-10_i-1472530833_i-137_i-1472531159_i-150_i-1472531208_%7D",
        "__utmt": "1",
        "__utma": "181774708.598983908.1472530330.1472530330.1472530330.1",
        "__utmb": "181774708.39.10.1472530330",
        "__utmc": "181774708",
        "__utmz": "181774708.1472530330.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
    }
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate, sdch',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
        'Cache - Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Host': 'bbs.pediy.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    meta = {
        'dont_redirect': True,
        'handle_httpstatus_list': [301, 302]
    }
    start_urls = [
        #"http://bbs.pediy.com/showthread.php?p=1443034",
        "http://bbs.pediy.com/showthread.php?t=212468"
    ]

    def get_next_url(self, oldUrl):
        '''
        返回下次迭代的url
        :param nowUrl:
        :return:
        '''
        l = oldUrl.split('=')
        oldID = int(l[1])
        newID = oldID - 1
        if newID == 0:
            return
        newUrl = l[0] + "=" + str(newID)
        return str(newUrl)

    def start_requests(self):
        """
        对初始url的处理
        :return:
        """
        for url in self.start_urls:
            yield scrapy.Request(url,
                             callback=self.parse, headers=self.headers,
                             cookies=self.cookies, meta=self.meta)

    def parse(self, response):
        """
        用以爬取主题贴的首页
        :param response:
        :return:
        """
        first_floor_flag = True
        selector = Selector(response)

        posts = selector.xpath('//*[@id="wrap"]')
        authors = selector.xpath('//*[@class="ccf"]')
        times = selector.xpath('//*[@id="table1"]')
        if not posts:
            print "bad url!"
            f = open('badurl.txt', 'a')
            f.write(response.url)
            f.write('\n')
            f.close
            next_url = self.get_next_url(response.url)
            if next_url != None:
                yield scrapy.Request(next_url,
                                 callback=self.parse, headers=self.headers,
                                 cookies=self.cookies, meta=self.meta)
            return
        i = 0
        for each in posts:
            item = PediyItem()
            if first_floor_flag == True:
                item['board'] = selector.xpath('//*[@class="tborder"]/tr/td[1]/table/tr[1]/td[3]/span[3]/a/text()').extract()[0]  # 因为extract()返回类型是list，所以此处都取[0]
                item['title'] = selector.xpath('//*[@class="tborder"]/tr/td[1]/table/tr[2]/td/strong/text()').extract()[0].replace('\r\n', '').replace(' ', '').replace('\n', '').replace('\t', '')
                item['floor'] = '1'
                first_floor_flag = False
            item['author'] = authors[i].xpath('div[1]/a/font/text()').extract()[0]
            try:
                item['time'] = times[i].xpath('tr/td[1]/div/text()').re(r'[0-9]+-[0-9]+-[0-9]+, [0-9]+:[0-9]+:[0-9]+')[0].replace('\r\n', '').replace(' ', '').replace('\n', '').replace('\t', '')
            except:
                try:
                    item['time'] = times[i].xpath('tr/td[1]/div/text()').re(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')[
                        0].replace('\r\n', '').replace(' ', '').replace('\n', '').replace('\t', '')
                except:
                    item['time'] = ''

            t_f = each.xpath('string(.)').extract()
            content = "".join(t_f)  # 将list转化为string
            item['href'] = response.url
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '').replace('\t', '')
            i += 1
            yield item

        pages = selector.xpath('//*[@class="pagenav"]')
        if pages:  # 如果pages不是空列表，说明该主题帖分页
            pages = pages[1].xpath('table/tr/td[1]/text()').re(r'[0-9]+')[1]  # 正则匹配出总页数
            for page_num in xrange(2, int(pages) + 1):
                yield scrapy.Request(response.url + "&page=" + str(page_num),
                                     callback=self.sub_parse, headers=self.headers,
                                     cookies=self.cookies, meta=self.meta)

        next_url = self.get_next_url(response.url)
        if next_url != None:
            yield scrapy.Request(next_url,
                                callback=self.parse, headers=self.headers,
                                 cookies=self.cookies, meta=self.meta)

    def sub_parse(self, response):
        """
        用以爬取主题贴除首页外的其他页
        :param response:
        :return:
        """
        selector = Selector(response)
        posts = selector.xpath('//*[@id="wrap"]')
        authors = selector.xpath('//*[@class="ccf"]')
        times = selector.xpath('//*[@id="table1"]')
        i = 0
        for each in posts:
            item = PediyItem()
            item['author'] = authors[i].xpath('div[1]/a/font/text()').extract()[0]
            item['time'] = times[i].xpath('tr/td[1]/div').re(r'[0-9]+-[0-9]+-[0-9]+, [0-9]+:[0-9]+:[0-9]+')[0].replace('\r\n', '').replace(' ', '').replace('\n', '').replace('\t', '')
            t_f = each.xpath('string(.)').extract()
            content = "".join(t_f)  # 将list转化为string
            href = response.url
            item['href'] = href.split('&')[0]
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '').replace('\t', '')
            i += 1
            yield item
