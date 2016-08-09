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
from doReply import doReply
from exPage import exPage

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 网站域名
domain = "bbs.eyuyan.com"
# 起始帖子id
tid_start = 10002
# 6.30日最后一个帖子id
tid_end = 10003 #312395
# 代理服务器
proxy_server = 'http://120.198.231.85:80'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "eyuyan"

'''
---------------------------------------------------------
'''

# 用于匹配日期的正则表达式
compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')
# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]
# 设置http报文的header信息
opener = urllib2.build_opener()
#Cookie = "e5da7_ipstate=1470716588; e5da7_winduser=AwMAU1YCa10DCgBaBgZVDFYFUFUMUFFRUwBQAQdSAwBcClAGBVUGag; e5da7_ck_info=%2F%09; e5da7_threadlog=%2C124%2C148%2C160%2C116%2C119%2C149%2C159%2C128%2C; e5da7_ol_offset=5917; e5da7_readlog=%2C312250%2C312400%2C312380%2C312392%2C312397%2C312396%2C312395%2C320749%2C; e5da7_cknum=BQACU1YFVgwFDGxrBQUCXFUDDFYEAVQCU1oAW1VSA1QHWwtTUAECUVQDVwk; e5da7_lastpos=index; e5da7_c_stamp=1470724890; e5da7_lastvisit=1448%091470724890%0"
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
#    ('Cookie',Cookie),
#    ('Connection','keep-alive')
    ]
# 以下两行用于设置代理，一般情况下无需使用
# proxy_handler = urllib2.ProxyHandler({'http':proxy_server})
# opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
for k in range(tid_start, tid_end):
    href = "http://" + domain + "/read.php?tid=" + str(k)
    try: 
        response = urllib2.urlopen(href)
        soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
        print soup
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(href + '    ----href bad')
        f.write('\n')
        f.close
        continue
    hidden = soup.find(attrs={'class':'f12 hidden quoteTips', 'id':'hidden_att_tpc'})
    if(hidden != None):
        f = open('needReply.txt','a')
        f.write(href)
        f.write('\n')
        f.close()
        continue
    try:
        _map = soup.find(name = 'div', attrs={'id':'breadCrumb'}).findAll(name = 'a')
    except:
        print href, '----deleted or not exsist or no power'
        f = open('badurl.txt','a')
        f.write(href + "    ----deleted or not exsist or no power")
        f.write('\n')
        f.close()
        continue
    board = _map[1].text
    title = _map[2].text
    p_look_content = soup.find(name ='div', attrs={'class':'readNum'})
    p_look_ems = p_look_content.findAll(name = 'em')
    p_page_content = soup.find(name='div',attrs = {'class':'pages'})
    if(p_page_content != None):
        a_content = p_page_content.findAll(name='a')
        p_page_url_init = "http://" + domain + "/" + a_content[0].get('href')[0:-1]
        p_card_num = p_look_ems[1].text
        p_page_end = int(p_card_num)/10 + 1
    else:
        p_page_end = 1
    if p_page_end > 400:
        exPage(soup, opener, coll, domain, href, p_page_end, p_page_url_init)
    p_look_num = p_look_ems[0].text
    newItem = {} # 初始化一个新帖子字典
    flag = True # 识别是不是楼主的flag
    for l in range(1, p_page_end+1):
        if(p_page_content != None):
            p_page_url = p_page_url_init + str(l)
        else:
            p_page_url = href
        try:
            response2 = urllib2.urlopen(p_page_url)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
            print 'located at ' + p_page_url
        except:
            print p_page_url + '   ---sub href bad'
            f = open('badurl.txt','a')
            f.write(p_page_url + '    ----sub href bad')
            f.write('\n')
            f.close()
            continue
        author_content = soup2.findAll(attrs={'class':'readName b'})
        time_content = soup2.findAll(attrs={'class':'tipTop s6'})
        floor_content = soup2.findAll(attrs={'class':'s2 b cp'})
        posts_contents = soup2.findAll(attrs={'class': 'tpc_content'})
        # 以下循环将正文部分处理成一整个字符串形式
        i = 0
        for post_contents in posts_contents:
            try:
                author = author_content[i].contents[1].string
                time = compiled_time.search(str(time_content[i])).group()
                floor = str(floor_content[i].string)
            except:
                print "ERROR:author or time or floor err"
                f = open('badurl.txt','a')
                f.write(p_page_url + '    ----author or time or floor bad')
                f.write('\n')
                f.close()
                continue
            post_contents = posts_contents[i].find(attrs={'class': 'f14 mb10'})
            if(post_contents == None): 
                print "ERROR:post_contents null"
                f = open('badurl.txt','a')
                f.write(p_page_url + '    ----post_contents null')
                f.write('\n')
                f.close()   
                continue
            lines = post_contents.encode('utf-8')
            lines = re.sub('[?]', '', lines)
            lines = re.sub('<span style=["]display:none["]>[^>]+>', '', lines)
            lines = re.sub('<font class=["]jammer["]>[^>]+>', '', lines)
            lines = re.sub('<(.*?)>', '', lines)
            lines = lines.strip()
            print lines
            ISOTIMEFORMAT = '%Y-%m-%d %X'
            spider_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
            if floor == u'楼主':
                floor = '0'
            elif floor == u'沙发':
                floor = '1'
            elif floor == u'板凳':
                floor = '2'
            elif floor == u'地板':
                floor = '3'
            try:
                floor_try = int(floor)
            except: 
                print "spesific floor"
                f = open('badurl.txt','a')
                f.write(p_page_url + '    ----spesific floor')
                f.write('\n')
                f.close()
                continue               
            # 整理数据
            if(i == 0 and flag == True):
                first_floor = {
                    'author':author,
                    'title':title.string,
                    'floor':floor,
                    'content':lines,
                    'href':href,
                    'board':board,
                    'time':time,
                    'ViewCount':p_look_num,
                    'ResCount':p_card_num,
                    'GmtDate':spider_time
                }
                newItem['0'] = first_floor
                flag = False
            else:
                other_floor = {
                    'content':lines,
                    'time':time,
                    'floor':floor,
                    'author':author
                }
                newItem[floor] = other_floor
            i += 1
    try:
        if not newItem:
            print "bad url!"
            f = open('badurl.txt','a')
            f.write(href + '    ----None dict')
            f.write('\n')
            f.close()
        else:
            coll.insert(newItem)
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(href + '    ----insert db wrong')
        f.write('\n')
        f.close()
        print "ERROR:数据库存储错误！"
print "网站", domain, "爬取结束！"
