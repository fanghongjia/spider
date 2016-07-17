# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import codecs
import sys
import math
import cookielib
import myTool
import MySQLdb

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 需要爬取的板块连接（注意该链接下的帖子是按照发帖时间进行排序的，且去掉最后的数字）
spiderUrl = "http://bbs.myhack58.com/thread.php?fid-70-page-"
# 入库存储的板块名称
board = "黑吧安全网原创文章软件区"
# 该板块内需要爬取的起始页号
page_start = 1
# 该板块内需要爬取的终止页号
page_end = 7
# 代理服务器
proxy_server = 'http://120.198.231.85:80'
# 数据库信息
mysqlHost = "172.26.253.87"
mysqlUser = "root"
mysqlPasswd = "YUgjBN"
mysqldatabase = "myhack58"

'''
---------------------------------------------------------
'''


'''
--------------------login settings-----------------------
'''
posturl = 'http://bbs.myhack58.com/login.php?'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
}

'''
---------------------------------------------------------
'''
# 数据库的连接信息
conn = MySQLdb.connect(
    host=mysqlHost,
    user=mysqlUser,
    passwd=mysqlPasswd,
    db=mysqldatabase,
    charset="utf8")
cursor = conn.cursor()
# 用于匹配日期的正则表达式
compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')
# 以下两行用于设置代理，一般情况下无需使用
# proxy_handler = urllib2.ProxyHandler({'http':proxy_server})
# opener = urllib2.build_opener(proxy_handler)
for k in range(page_start, page_end):
    jumpurl = spiderUrl + str(k) + ".html"
    postData = {
        'lgt':'0',
        'pwuser':'wtfa',
        'pwpwd':'k1234567890',
        'question':'0',
        'customquest':'',
        'answer':'',
        'hideid':'0',
        'forward':'',
        'jumpurl':jumpurl,
        'step':'2',
        'cktime':'31536000'
    }
    postData = urllib.urlencode(postData)
    request = urllib2.Request(posturl, postData, headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
    tagA = soup.findAll(name='h3')
    # 依次解析每一个帖子标题
    for title in tagA:
        title = title.find(name = 'a')
        # 从标题中提取帖子的链接，访问该链接从中解析出帖子更多信息
        href = urllib.unquote(title['href'])
        href = "http://bbs.myhack58.com/"+href
        myTool.myTool(href, title, board, cursor, conn)
cursor.close()
conn.close()
print "板块 " + board + " 爬取结束！"
