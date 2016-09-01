#-*-coding:utf8-*-

import sys
import time
import random
import scrapy
from scrapy.selector import Selector
from www52fzba.items import Www52FzbaItem  # 报错是pyCharm的原因

reload(sys)
sys.setdefaultencoding('utf-8')

class www52fzbaSpider(scrapy.spiders.Spider):
    name = "www52fzba"  # 在命令行中输入scrapy crawl bbs125启动此爬虫
    allowed_domains = ["52fzba.com"]  # 非此域名的url不爬
    cookies = {
        "PHPSESSID": "27qlp2fh058nrt33d8doepj6s6",
        "32Kd_fe26_saltkey": "Ba87Oi63",
        "32Kd_fe26_lastvisit": "1472690888",
        "32Kd_fe26_home_diymode": "1",
        "32Kd_fe26_forum_lastvisit": "D_4_1472695106",
        "32Kd_fe26_visitedfid": "41D4",
        "32Kd_fe26_viewid": "tid_452326",
        "32Kd_fe26_sendmail": "1",
        "_gat": "1",
        "32Kd_fe26_zychatmsg": "484525",
        "32Kd_fe26_onlineusernum": "816",
        "32Kd_fe26_sid": "x7SUDp",
        "__asc": "d2056c8c156e364537a3d71aefb",
        "__auc": "af61dae41560d595c8e359cb7e9",
        "_ga": "GA1.2.922402234.1469102774",
        "32Kd_fe26_smile": "1D1",
        "32Kd_fe26_lastact": "1472696310%09plugin.php%09"
    }
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate, sdch',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
        'Cache - Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    meta = {
        'dont_redirect': True,
        'handle_httpstatus_list': [301, 302]
    }
    start_urls = [
        "http://www.52fzba.com/thread-7639738-1-1.html"  # 7654271
    ]

    def get_next_url(self, oldUrl):
        '''
        返回下次迭代的url
        :param nowUrl:
        :return:
        '''
        l = oldUrl.split('-')
        oldID = int(l[1])
        newID = oldID - 1
        if newID == 0:
            return
        newUrl = l[0] + "-" + str(newID) + "-" + l[2] + "-" + l[3]
        return str(newUrl)

    def start_requests(self):
        """
        对初始url的处理
        :return:
        """
        yield scrapy.Request(self.start_urls[0],
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

        table = selector.xpath('//*[starts-with(@id, "pid")]')  # 取出所有的楼层
        if not table:
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
        for each in table:
            item = Www52FzbaItem()
            if first_floor_flag == True:
                item['board'] = selector.xpath('//*[@id="pt"]/div/a[4]/text()').extract()[0]  # 因为extract()返回类型是list，所以此处都取[0]
                item['title'] = selector.xpath('//*[@id="thread_subject"]/text()').extract()[0]
                item['floor'] = '1'
                ISOTIMEFORMAT = '%Y-%m-%d %X'
                item['GmtDate'] = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
                item['ViewCount'] = selector.xpath('//*[@class="xi1"]/text()').extract()[0]
                item['ResCount'] = selector.xpath('//*[@class="xi1"]/text()').extract()[1]
                first_floor_flag = False
            try:
                item['author'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/div[@class="pi"]/div[@class="authi"]/a/text()').extract()[0]
            except:
                item['author'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/div[@class="pi"]/text()').extract()[0]
                continue
            item['time'] = each.xpath('tr[1]/td[@class="plc"]/div[@class="pi"]').re(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')[0]
            t_f = each.xpath('.//td[@class="t_f"]').xpath('string(.)').extract()
            content = "".join(t_f)  # 将list转化为string
            href_tmp = response.url.split('-')
            item['href'] = href_tmp[0] + '-' + href_tmp[1] + '-1-1.html'
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '')
            yield item
        pages = selector.xpath('//*[@id="pgt"]/div/div/label/span')
        if pages:  # 如果pages不是空列表，说明该主题帖分页
            pages = pages[0].re(r'[0-9]+')[0]  # 正则匹配出总页数
            print pages
            tmp = response.url.split('-')
            for page_num in xrange(2, int(pages) + 1):
                sub_url = tmp[0] + '-' + tmp[1] + '-' + str(page_num) + '-' + tmp[3]
                yield scrapy.Request(sub_url,
                                     callback=self.sub_parse, headers=self.headers,
                                     cookies=self.cookies, meta=self.meta)
        next_url = self.get_next_url(response.url)
        if next_url != None:
            yield scrapy.Request(next_url,
                                callback=self.parse, headers=self.headers,
                                cookies=self.cookies, meta=self.meta)
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
        table = selector.xpath('//*[starts-with(@id, "pid")]')  # 取出所有的楼层
        for each in table:
            item = Www52FzbaItem()
            try:
                item['author'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/div[@class="pi"]/div[@class="authi"]/a/text()').extract()[0]
            except:
                item['author'] = each.xpath('tr[1]/td[@class="pls"]/div[@class="pls favatar"]/div[@class="pi"]/text()').extract()[0]
                continue
            item['time'] = each.xpath('tr[1]/td[@class="plc"]/div[@class="pi"]').re(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')[0]
            t_f = each.xpath('.//td[@class="t_f"]/text()').extract()
            content = "".join(t_f)
            href_tmp = response.url.split('-')
            item['href'] = href_tmp[0] + '-' + href_tmp[1] + '-1-1.html'
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '')
            yield item
