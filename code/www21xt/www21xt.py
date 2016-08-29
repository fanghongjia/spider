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
domain = "www.21xt.net"
# 起始tid
tid_start = 1000
# 6月30最后的tid
tid_end = 1149 #5247
# 代理服务器
# proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "www21xt"

'''
---------------------------------------------------------
'''

# 用于匹配日期的正则表达式
compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')
# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]
# 设置http报文的header信息
opener = urllib2.build_opener()
Cookie = "safedog-flow-item=; touclick-KeyboardBehavior=156C5C5384DJQW8YQWN4SVX3EB590BTK; vh2L_2132_sid=SlC2oW; vh2L_2132_saltkey=kqf3ABzB; vh2L_2132_lastvisit=1472216125; vh2L_2132_lastact=1472220653%09misc.php%09patch; vh2L_2132_secqaa=5.20270babc3e547564d; vh2L_2132_check_key=; vh2L_2132_check_address=; vh2L_2132_seccode=6.0b18b569d51a41fd98; vh2L_2132_ulastactivity=9737Seswzv%2Bqm91CLCClFUsk%2Fb25G6%2Bxk7OSywujOMWSX18m%2BbbC; vh2L_2132_auth=edb2CrXHu64d7lZoUlxBDeXkJsP%2FJS9n59VsLPQOFsQxHy2%2FKs%2FCPHGOYrgTWpUZKUfNUn8XWPVGic3V8kYoqHYh; vh2L_2132_lastcheckfeed=4685%7C1472220020; vh2L_2132_lip=222.175.198.13%2C1472220473; vh2L_2132_connect_is_bind=0; vh2L_2132_nofavfid=1; vh2L_2132_noticeTitle=1; vh2L_2132_study_nge_extstyle=auto; vh2L_2132_study_nge_extstyle_default=auto; vh2L_2132_st_t=4685%7C1472220051%7Caa204ad3cb69cd39c2a084cb49d54c1a; vh2L_2132_forum_lastvisit=D_2_1472220051; vh2L_2132_visitedfid=2; vh2L_2132_connect_not_sync_feed=1; vh2L_2132_connect_not_sync_t=1; vh2L_2132_sendmail=1; vh2L_2132_checkpm=1; tjpctrl=1472222397999; vh2L_2132_onlineusernum=50"
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
    ('Cookie',Cookie),
    ('Connection','keep-alive')
    ]
# 以下两行用于设置代理，一般情况下无需使用
# proxy_handler = urllib2.ProxyHandler({'http':proxy_server})
# opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
for k in xrange(tid_end, tid_start, -1):
    for s in xrange(1, random.randint(2,10)):
        time.sleep(1)
        print 'sleep'
    href = "http://" + domain +"/thread-" + str(k) + "-1-1.html"
    try: 
        response2 = urllib2.urlopen(href)
        soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
    except:
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
        p_page_content = soup2.find(attrs={'class':'pgt'}).find(attrs={'class':'pg'})
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(href + '    ----None posts')
        f.write('\n')
        f.close()
        continue
    if(p_page_content != None):
        try:
            p_page_url_init = "http://" + domain +"/thread-" + str(k)
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
	for s in xrange(1, random.randint(2,10)):
            time.sleep(1)
            print 'sleep'
        if(p_page_content != None):
            p_page_url = p_page_url_init + "-" + str(l) + "-1.html"
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
                try:
                    author = posts[2*(i-1)].contents[1].contents[0].text
                except:
                    author = (posts[2*(i-1)].text)[2:] #处理匿名的情况
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
            # 整理数据
            if(i == 1 and flag == True):
                first_floor = {
                    'author':author,
                    'title':title,
                    'floor':'1',
                    'content':lines,
                    'href':href,
                    'board':board,
                    'time':_time
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
