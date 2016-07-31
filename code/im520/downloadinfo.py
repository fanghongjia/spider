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

#
# downloadinfo
# Description: 下载保存用户信息
# url: 用户信息的url
# domian: 网站的域名，例：bbs.2cto.com
# Cookie: 登录所获取的Cookie字符串
# coll： Mongodb数据库的操作手柄
#
def downloadinfo(url, domain, Cookie, coll):
    # 设置http报文的header信息
    opener = urllib2.build_opener()
    opener.addheaders = [
            ('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'),
            ('Cookie',Cookie),
            ('Connection','keep-alive')
        ]
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url) #打开这个资料页
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8") #解析这个资料页
    user = {} #声明一个空字典
    user['url'] = url
    top = soup.find(attrs = {'class':'bm_c u_profile'})
    if top == None:
        print "This uid is not exist!"
        f = open('baduid.txt','a')
        f.write(url)
        f.write('\n')
        return
    counts = top.findAll(attrs = {'class':'pbm mbm bbda cl'})
    for count in counts:
        mbn = count.find(attrs = {'class':'mbn'})
        mbn_text = mbn.text
        if mbn_text == u'勋章':
            print mbn_text
        elif mbn_text == u'管理以下版块':
            print mbn_text
        elif mbn_text == u'活跃概况':
            print mbn_text
        else:
            print mbn_text
    cl = top.find(attrs = {'class':'cl', 'id':'psts'})
    pfl_lis = cl.find(attrs = {'class':'pf_l'}).findAll(name = 'li')
    ems = cl.find(attrs = {'class':'pf_l'}).findAll(name = 'em')
    i = 0
    for pfl_li in pfl_lis:
        key_temp = ems[i].text
        value_temp = pfl_li.text
        value_temp.replace(key_temp, '')
        print key_temp, value_temp
        i = i + 1
    
    # coll.insert(user)


