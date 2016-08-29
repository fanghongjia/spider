#-*-coding:utf8-*-

import sys
import time
import random
import scrapy
from scrapy.selector import Selector
from zhuangxiuzhai.items import ZhuangxiuzhaiItem

reload(sys)
sys.setdefaultencoding('utf-8')

class zhuangxiuzhaiSpider(scrapy.spiders.Spider):
    name = "zhuangxiuzhai"  # 在命令行中输入scrapy crawl zhuangxiuzhai启动此爬虫
    allowed_domains = ["zhuangxiuzhai.com"]  # 非此域名的url不爬
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate, sdch',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
        'Cache - Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Host': 'www.zhuangxiuzhai.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    start_urls = [
        "http://www.zhuangxiuzhai.com/html/quantaomoban/zhuanyeban/6399.html",
        "http://www.zhuangxiuzhai.com/html/quantaomoban/jichuban/7384.html",
        "http://www.zhuangxiuzhai.com/html/quantaomoban/imoban/5601.html",
        "http://www.zhuangxiuzhai.com/html/quantaomoban/yijian/4194.html",
        "http://www.zhuangxiuzhai.com/html/miaoshumoban/quan/2070.html",
        "http://www.zhuangxiuzhai.com/html/miaoshumoban/daima/4178.html",
        "http://www.zhuangxiuzhai.com/html/miaoshumoban/fenlan/4048.html",
        "http://www.zhuangxiuzhai.com/html/miaoshumoban/tongyong/1838.html",
        "http://www.zhuangxiuzhai.com/html/miaoshumoban/wenan/7649.html",
        "http://www.zhuangxiuzhai.com/html/tbzhuangxiusucai/dianzhao/5848.html",
        "http://www.zhuangxiuzhai.com/html/zhuangxiusucai/phone/3803.html",
        "http://www.zhuangxiuzhai.com/html/zhuangxiusucai/beijingtu/4878.html",
        "http://www.zhuangxiuzhai.com/html/zhuangxiusucai/fenlei/4613.html",
        "http://www.zhuangxiuzhai.com/html/zhuangxiusucai/shoucang/8102.html",
        "http://www.zhuangxiuzhai.com/html/zhuangxiusucai/yingyeshijian/4879.html",
        "http://www.zhuangxiuzhai.com/html/zhuangxiusucai/huanying/4614.html",
        "http://www.zhuangxiuzhai.com/html/zhuangxiusucai/wufen/3988.html",
        "http://www.zhuangxiuzhai.com/html/zhuangxiusucai/qita/4276.html",
        "http://www.zhuangxiuzhai.com/html/daima/cuxiao/5661.html",
        "http://www.zhuangxiuzhai.com/html/daima/kefu/5959.html",
        "http://www.zhuangxiuzhai.com/html/daima/tuangoumoban/5569.html",
        "http://www.zhuangxiuzhai.com/html/daima/dapeimoban/4651.html",
        "http://www.zhuangxiuzhai.com/html/daima/daohang/6936.html",
        "http://www.zhuangxiuzhai.com/html/daima/bottom/4195.html",
        "http://www.zhuangxiuzhai.com/html/daima/gonggaolan/5660.html",
        "http://www.zhuangxiuzhai.com/html/daima/qita/6937.html",
        "http://www.zhuangxiuzhai.com/html/jiaocheng/3524.html",
        "http://www.zhuangxiuzhai.com/html/jiaocheng/ps/7645.html",
        "http://www.zhuangxiuzhai.com/html/jiaocheng/sheying/2208.html",
        "http://www.zhuangxiuzhai.com/html/psdsucai/shouye/5572.html",
        "http://www.zhuangxiuzhai.com/html/psdsucai/haibao/5037.html",
        "http://www.zhuangxiuzhai.com/html/psdsucai/zhitongche/4456.html",
        "http://www.zhuangxiuzhai.com/html/psdsucai/zuanzhan/1780.html",
        "http://www.zhuangxiuzhai.com/html/psdsucai/shuiyin/2102.html",
        "http://www.zhuangxiuzhai.com/html/psdsucai/qita/5518.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/dongtai/8194.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/guize/4923.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/kaidian/5222.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/m/4836.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/fenxiang/8279.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/tuiguang/7490.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/fangdao/5833.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/yunying/7666.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/zhifubao/4677.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/huoyuan/1270.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/tmall/8282.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/ruanjian/7896.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/dianshang/7814.html",
        "http://www.zhuangxiuzhai.com/html/taobaodaxue/zhaopin/8058.html",
        "http://www.zhuangxiuzhai.com/html/taobaogongju/ziliao/sp/4725.html"
    ]

    def parse(self, response):
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        spider_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
        selector = Selector(response)
        item = ZhuangxiuzhaiItem()
        item['url'] = response.url
        item['title'] = selector.xpath('//*[@id="code_index_warp"]/div[@class="code_index_warp_left"]/div[@class="list_article"]/div[@class="search_title"]/h1/text()').extract()[0]
        item['board'] = selector.xpath('//*[@id="code_index_warp"]/div[@class="code_index_warp_left"]/div[@class="list_article"]/div[@class="list_article_title"]/a[3]/text()').extract()[0]
        contentlist = selector.xpath('//*[@id="code_index_warp"]/div[@class="code_index_warp_left"]/div[@class="list_article"]/div[@class="code_down_content"]').xpath('string(.)').extract()
        content = "".join(contentlist)  # 将list转化为string
        item['content'] = content.replace('\r\n', '').replace(' ', '').replace('\n', '').replace('\t', '')
        item['GmtDate'] = spider_time
        yield item
        try:
            next_url = selector.xpath('//*[@id="code_index_warp"]/div[@class="code_index_warp_left"]/div[@class="list_article"]/div[@class="code_down_Thenext"]/p[1]/a/@href').extract()[0]
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers)
        except:
            f = open('end.txt', 'a')
            f.write('end one board')
            f.write('\n')
            f.close
            print 'on board end'
