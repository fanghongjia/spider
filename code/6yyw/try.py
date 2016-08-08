# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import pymongo
import re
import codecs
import sys
import math
import time
reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')

# 设置http报文的header信息
opener = urllib2.build_opener()
opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36')           
        ]
urllib2.install_opener(opener)
response = urllib2.urlopen('http://www.6yyw.com') #打开这个资料页
soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
print soup
