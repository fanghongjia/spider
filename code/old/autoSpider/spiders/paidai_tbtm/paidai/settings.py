# -*- coding: utf-8 -*-
import random
# Scrapy settings for paidai project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'paidai'

SPIDER_MODULES = ['paidai.spiders']
NEWSPIDER_MODULE = 'paidai.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'paidai (+http://www.yourdomain.com)'

#静止cookies访问,防止被ban
COOKIES_ENABLED = False

#设置延迟
DOWNLOAD_DELAY = random.uniform(2.0, 5.0)    
RANDOMIZE_DOWNLOAD_DELAY = True

ITEM_PIPELINES = {
    'paidai.pipelines.PaidaiPipeline' : 300
    }

#取消默认的useragent,使用新的useragent
DOWNLOADER_MIDDLEWARES = {
       'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
       'paidai.spiders.rotate_useragent.RotateUserAgentMiddleware' : 400,

        #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
        #'paidai.spiders.midproxy.ProxyMiddleware': 100,
   }


