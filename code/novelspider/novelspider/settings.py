# -*- coding: utf-8 -*-

# Scrapy settings for novelspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'novelspider'

SPIDER_MODULES = ['novelspider.spiders']
NEWSPIDER_MODULE = 'novelspider.spiders'

ITEM_PIPELINES = ['novelspider.pipelines.NovelspiderPipeline'] # to include the class named in pipelines.py

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 12345
MONGODB_DBNAME = 'books'
MONGODB_DOCNAME = 'daomubiji'

