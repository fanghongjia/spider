# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import pymongo
import redis
import re
import codecs
import sys
import math
import time
import random
from doReply import doReply
from exPage import exPage

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 爬取的网站域名
domain = "bbs.d3botdb.com"
# 起始tid
tid_start = 1
# 6月30最后的tid
tid_end = 11924#12172
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "d3botdb"

'''
---------------------------------------------------------
'''

# 用于匹配日期的正则表达式
compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')

# mongodb数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

# redis代理数据库链接信息
pool = redis.ConnectionPool(host='172.26.253.99', port=6379,password='nslab')
r = redis.StrictRedis(connection_pool=pool,charset='utf-8')

open_it = 0  # urlopen次数迭代器
proxy_it = 0  # 代理数组迭代器
changeProxy = 10  # 换代理的标识，10贴一换或打不开网页时换
for k in xrange(tid_end, tid_start, -1):
    if changeProxy == 10:
        proxys = eval(r.get('0')) # 获得100个代理IP
        proxy_server = proxys[proxy_it]
        proxy_it += 1
        if proxy_it == 100:
            proxy_it = 0
        changeProxy = 0
    else:
        changeProxy += 1
    # 以下两行用于设置代理
    print proxy_server
    proxy_handler = urllib2.ProxyHandler({'http':proxy_server})
    opener = urllib2.build_opener(proxy_handler)

    Cookie = "1hJj_2132_saltkey=Q5DNsS7p; 1hJj_2132_lastvisit=1472354628; 1hJj_2132_ulastactivity=7ad1MUYjFFKPI1MG9ycFl7iwTSmh97qQKis3KhpxxBKvRz9tCOip; 1hJj_2132_lastcheckfeed=24932%7C1472358266; 1hJj_2132_security_cookiereport=34710%2FwDKWULXJ2cuiZ5U5eoe%2B0DhKYz2MPTES%2Btoy6MJ78bQqi0; 1hJj_2132_auth=73ecbhIGp5WmrC7%2FgKN25mm4O3U8CHm2psQ7Vta2R554AKS2FxS9CGm8CCSvdMkOUTAxXd5aCaX69IJloG4gnK%2B8EQ; 1hJj_2132_nofavfid=1; tjpctrl=1472360072671; 1hJj_2132_forum_lastvisit=D_39_1472358628D_63_1472358806D_52_1472358825; 1hJj_2132_lip=202.102.144.8%2C1472358266; 1hJj_2132_sendmail=1; 1hJj_2132_visitedfid=52D72D63D39D117D120; 1hJj_2132_viewid=tid_10661; 1hJj_2132_sid=SlbgZg; pgv_pvi=6678356844; pgv_info=ssi=s9546479629; 1hJj_2132_smile=1D1; 1hJj_2132_lastact=1472359831%09misc.php%09patch"

    # 设置http报文的header信息
    opener.addheaders = [
        ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
        ('Cookie',Cookie),
        ('Connection','keep-alive')
        ]
    urllib2.install_opener(opener)
    href = "http://" + domain +"/forum.php?mod=viewthread&tid=" + str(k) + "&extra=page%3D1"
    try: 
        response2 = urllib2.urlopen(href, timeout=10)
        soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
    except:
        open_it += 1
        changeProxy = 10  # 此时应换代理
        k -= 1
        if open_it >= 10:
            open_it = 0
            print "bad url!"
            f = open('badurl.txt','a')
            f.write(href + '    ----href bad')
            f.write('\n')
            f.close
        continue
    hidden = soup2.find(attrs={'class':'locked'})
    if hidden != None:
        if hidden.find(name='a') != None:
            doReply(href, domain, Cookie)
    try:
        p_page_content = soup2.find(attrs={'class':'pgt'})
        if p_page_content != None:
            p_page_content = p_page_content.find(attrs = {'class':'pg'})
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(href + '    ----None posts')
        f.write('\n')
        f.close()
        continue
    if(p_page_content != None):
        try:
            p_page_url_init = "http://" + domain +"/forum.php?mod=viewthread&tid=" + str(k) + "&extra=page%3D1&page="
        except:
            print "bad url!"
            f = open('badurl.txt','a')
            f.write(href + '    ----p_page_init bad')
            f.write('\n')
            f.close()
            continue
        p_page_end = p_page_content.find(name='span').string
        compiled_page = re.compile(r'[0-9]+')
        p_page_end = int(compiled_page.search(str(p_page_end)).group())
        print 'this post has ', p_page_end, 'pages.'
        if p_page_end > 400:
            exPage(soup2, opener, coll, domain, href, p_page_end, p_page_url_init)
            continue
    else:
        p_page_end = 1
    try:
        board = soup2.find(attrs = {'class':'bm cl'}).findAll(name = 'a')[-2].text
        title = soup2.find(attrs = {'id':'thread_subject'}).text
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(href + '    ----board or title bad')
        f.write('\n')
        f.close()
        continue
    newItem = {} # 初始化一个新帖子字典
    flag = True # 识别是不是楼主的flag
    floor = 1
    for l in range(1, p_page_end+1):
        if(p_page_content != None):
            p_page_url = p_page_url_init + str(l)
        else:
            p_page_url = href
        try:
            response3 = urllib2.urlopen(p_page_url)
            soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
            print 'located at ' + p_page_url
        except:
            f = open('badurl.txt','a')
            f.write(p_page_url + '    ----sub herf bad')
            f.write('\n')
            f.close()
            continue
        posts = soup3.findAll(attrs={'class': 'pi'})
        posts_contents = soup3.findAll(attrs={'class': 't_f'})
        # 以下循环将正文部分处理成一整个字符串形式
        i = 1
        for post_contents in posts_contents:
            try:
                author = posts[2*(i-1)].contents[1].contents[0].string
                _time = compiled_time.search(str(posts[2*(i-1)+1])).group()
            except:
                print "ERROR:获取作者、时间、楼层信息出错！"
                f = open('badurl.txt','a')
                f.write(p_page_url + '    ----author or time or floor bad')
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
            if(i == 1 and flag == True):
                hm = soup2.find(attrs = {'class':'hm ptn'})
                if hm == None:
                    print "bad url!"
                    f = open('badurl.txt','a')
                    f.write(href + '    ----no post or deleted')
                    f.write('\n')
                    f.close
                    continue
                p_num = re.findall(r'[0-9]+', hm.text, re.I)
                p_look_num = p_num[0]
                p_rep_num = p_num[1]
                ISOTIMEFORMAT = '%Y-%m-%d %X'
                spider_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
                first_floor = {
                    'author':author,
                    'title':title,
                    'floor':'1',
                    'content':lines,
                    'href':href,
                    'board':board,
                    'time':_time,
                    'ViewCount':p_look_num,
                    'ResCount':p_rep_num,
                    'GmtDate':spider_time
                }
                print "爬到",_time,title,"了"
                newItem['1'] = first_floor
                flag = False
            else:
                other_floor = {
                    'content':lines,
                    'time':_time,
                    'floor':str(floor),
                    'author':author
                }
                newItem[str(floor)] = other_floor
            i += 1
            floor += 1
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
print "网站" + domain + " 爬取结束！"
print 'simple-> ', str(time2 - time1)
