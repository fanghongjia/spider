#-*-coding:utf8-*-

import sys
import time
import random
import scrapy
from scrapy.selector import Selector
from bbs125.items import Bbs125Item  # 报错是pyCharm的原因

reload(sys)
sys.setdefaultencoding('utf-8')

class bbs125Spider(scrapy.spiders.Spider):
    name = "bbs125"  # 在命令行中输入scrapy crawl bbs125启动此爬虫
    allowed_domains = ["125.la"]  # 非此域名的url不爬
    start_urls_init = "http://bbs.125.la/forum.php?mod=viewthread&tid="
    sub_urls_init = "http://bbs.125.la/thread-"
    tid = 13930130
    END_TID = 13930080  # 终止的tid
    cookies = {
        'lDlk_ecc9_ip': '221.2.164.39',
        'PHPSESSID': '9ic9a8728ru38es5efhqikulg4',
        'tjpctrl': '1472091443618',
        'lDlk_ecc9_saltkey': 'f595E2LZ',
        'lDlk_ecc9_lastvisit': '1472086343',
        'lDlk_ecc9_sendmail': '1',
        'lDlk_ecc9_ulastactivity': '00a3uboPa%2Fb3i83xebmoYKwWSXsAUbpOvlP8MB5fLIqdZQm%2BzDhQ',
        'lDlk_ecc9_auth': 'fe31nyauvpMNAoqsxlSujJV1aQ28mogeyJzVGzioc%2F%2BFw5e276KGJU%2F9EIzhB1efMGxLS610yO0zRRfDAb6vyK2h5lw',
        'lDlk_ecc9_lastcheckfeed': '363083%7C1472089969',
        'lDlk_ecc9_checkfollow': '1',
        'lDlk_ecc9_lip': '221.2.164.42%2C1472089969',
        'lDlk_ecc9_nofavfid': '1',
        'lDlk_ecc9_onlineusernum': '3877',
        'lDlk_ecc9_wx_from': '69a8k2Vtbtgh%2F7iBviQXUDcSqS1Yfupsaz6MvSXVbUeZq4eh90MB',
        'lDlk_ecc9_myrepeat_rr': 'R0',
        'lDlk_ecc9_sid': 'QUwhJ6',
        'Hm_lvt_fa32dadde3745af309b587b38d20ea1d': '1471931855,1471933872,1471999704,1472087053',
        'Hm_lpvt_fa32dadde3745af309b587b38d20ea1d': '1472089970',
        'lDlk_ecc9_connect_is_bind': '0',
        'lDlk_ecc9_checkpm': '1',
        'lDlk_ecc9_lastact': '1472089970%09like.php%09'
    }
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate, sdch',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
        'Cache - Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Host': 'bbs.125.la',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    meta = {
        'dont_redirect': True,
        'handle_httpstatus_list': [301, 302]
    }
    start_urls = [
        start_urls_init + str(tid)
    ]

    def start_requests(self):
        """
        对初始url的处理
        :return:
        """
        # 此处写作return会报错，原因不明
        yield scrapy.Request(bbs125Spider.start_urls_init + str(bbs125Spider.tid),
                             callback=self.parse, headers=self.headers,
                             cookies=self.cookies, meta=self.meta)

    def parse(self, response):
        """
        用以爬取主题贴的首页
        :param response:
        :return:
        """
        tid = bbs125Spider.tid
        floor = 1
        first_floor_flag = True
        selector = Selector(response)

        # 如有回复可见的隐藏区域，进行回复
        locked = selector.xpath('//*[@class="locked"]')
        if locked:
            re_a = locked.xpath('a/text()')
            if re_a and re_a.extract()[0] == u'回复':
                form_action = selector.xpath('//*[@id="fastpostform"]/@action').extract()[0]
                action = "http://www." + self.allowed_domains[0] + "/" + form_action + "&inajax=1"
                replys = [
                    '6666666666666666666',
                    'I%20want%20to%20look%20what%20locked%20by%20louzhu.',
                    'There%20looking%20like%20exist%20something%20intersting.',
                    'learn%20something%20from%20this%20post.',
                    'Let%20me%20see%20what%20lz%20locked!',
                    '%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B',
                    '%E7%9C%8B%E7%9C%8B%E6%A5%BC%E4%B8%BB%E9%9A%90%E8%97%8F%E4%BA%86%E4%BB%80%E4%B9%88',
                    '%E7%9C%8B%E7%9C%8B%E5%AD%A6%E4%B9%A0%E4%B8%80%E4%B8%8B',
                    '%E5%AD%A6%E4%B9%A0%E5%AD%A6%E4%B9%A0%E5%AD%A6%E4%B9%A0',
                    '%E5%AD%A6%E4%B9%A0%E4%B8%8B%E5%95%8A%E5%AD%A6%E4%B9%A0',
                    '%E5%AD%A6%E4%B9%A0%E5%AD%A6%E4%B9%A0%E3%80%82%E3%80%82',
                    '%E6%9D%A5%E5%AD%A6%E4%B9%A0%EF%BC%8C%E7%9C%8B%E7%9C%8B',
                    '%E5%9B%9E%E5%A4%8D%E7%9C%8B%E7%9C%8B%20%E6%9C%89%E7%94%A8%E4%B8%8D',
                    'Good!!!!!!!!',
                    '%E6%A5%BC%E4%B8%BB%E8%BE%9B%E8%8B%A6%E4%BA%86%E9%80%81%E8%8A%B1',
                    '%E6%88%91%E6%9D%A5%E7%9C%8B%E7%9C%8B%E5%AD%A6%E4%B9%A0',
                    '%E7%9C%8B%E7%9C%8B%E6%80%8E%E4%B9%88%E6%A0%B7',
                    '%E5%A5%BD%E5%A5%BD%E5%AD%A6%E4%B9%A0',
                    '%E5%AD%A6%E4%B9%A0%E4%B8%80%E4%B8%8B%E3%80%82%E5%AD%A6%E4%B9%A0%E4%B8%80%E4%B8%8B%E3%80%82',
                    '%E5%AD%A6%E4%B9%A0%E5%AD%A6%E4%B9%A0~~~~~~~~~~~~~~~~~~~~~~~~'
                ]  # url编码的一些回复，防止被管理员识别是机器回复
                reply = replys[random.randint(0, 19)]
                formdata = {
                    'formhash': selector.xpath('//*[@id="fastpostform"]/table/tr/td[2]/input[2]/@value').extract()[0],
                    'usesig': selector.xpath('//*[@id="fastpostform"]/table/tr/td[2]/input[3]/@value').extract()[0],
                    'subject': selector.xpath('//*[@id="fastpostform"]/table/tr/td[2]/input[4]/@value').extract()[0],
                    'posttime': selector.xpath('//*[@id="posttime"]/@value').extract()[0],
                    'message': reply
                }
                yield scrapy.FormRequest(action, callback=self.parse,
                                         headers=self.headers,
                                         cookies=self.cookies,
                                         meta=self.meta,
                                         formdata=formdata)
                return

        table = selector.xpath('//*[@class="plhin"]')  # 取出所有的楼层
        if not table:
            print "bad url!"
            f = open('badurl.txt', 'a')
            f.write(bbs125Spider.start_urls_init + str(tid))
            f.write('\n')
            f.close
            bbs125Spider.tid -= 1
            yield scrapy.Request(bbs125Spider.start_urls_init + str(bbs125Spider.tid),
                                 callback=self.parse, headers=self.headers,
                                 cookies=self.cookies, meta=self.meta)
            return
        for each in table:
            item = Bbs125Item()
            if first_floor_flag == True:
                item['board'] = selector.xpath('//*[@id="pt"]/div/a[4]/text()').extract()[0]  # 因为extract()返回类型是list，所以此处都取[0]
                item['title'] = selector.xpath('//*[@id="thread_subject"]/text()').extract()[0]
                first_floor_flag = False
            item['author'] = each.xpath('tr/td[@class="pls"]/div[@class="pls favatar"]/div[@class="pi"]/div[@class="authi"]/a/text()').extract()[0]
            item['time'] = each.xpath('tr/td[@class="plc"]/div[@class="pi"]').re(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')[0]
            t_f = each.xpath('.//td[@class="t_f"]').xpath('string(.)').extract()
            content = "".join(t_f)  # 将list转化为string
            # item['href'] = response.url也可
            item['href'] = selector.xpath('//*[@id="pt"]/div/a[5]/@href').extract()[0]
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '')
            item['floor'] = str(floor)
            floor += 1
            yield item
        pages = selector.xpath('//*[@id="pgt"]/div/div/label/span')
        if pages:  # 如果pages不是空列表，说明该主题帖分页
            print "============================================="
            print pages
            pages = pages.re(r'[0-9]+')[0]  # 正则匹配出总页数
            for page_num in xrange(2, int(pages) + 1):
                yield scrapy.Request(bbs125Spider.sub_urls_init + str(tid) + '-' + str(page_num) + '-1.html',
                                     callback=self.sub_parse, headers=self.headers,
                                     cookies=self.cookies, meta=self.meta)
        if bbs125Spider.tid == bbs125Spider.END_TID:
            return  # 退出爬虫
        bbs125Spider.tid -= 1
        yield scrapy.Request(bbs125Spider.start_urls_init + str(bbs125Spider.tid),
                             callback=self.parse, headers=self.headers,
                             cookies=self.cookies, meta=self.meta)

    def sub_parse(self, response):
        """
        用以爬取主题贴除首页外的其他页
        :param response:
        :return:
        """
        print "||||||||||||||||||||||||||||||||||||||||||||"
        selector = Selector(response)
        table = selector.xpath('//*[@class="plhin"]')
        for each in table:
            item = Bbs125Item()
            item['author'] = each.xpath('tr/td[@class="pls"]/div[@class="pls favatar"]/div[@class="pi"]/div[@class="authi"]/a/text()').extract()[0]
            item['time'] = each.xpath('tr/td[@class="plc"]/div[@class="pi"]').re(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')[0]
            t_f = each.xpath('.//td[@class="t_f"]/text()').extract()
            content = "".join(t_f)
            item['href'] = selector.xpath('//*[@id="pt"]/div/a[5]/@href').extract()[0]
            item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '')
            yield item
