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
domain = "www.90houqq.com"
# 起始tid
tid_start = 1
# 6月30最后的tid
tid_end = 1205 #21523
# 代理服务器
# proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "www90houqq"

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
Cookie = "__cfduid=d2855ec313ade9a1251b16cb35a8e5b081472286067; XKwi_2132_saltkey=r86j2RWJ; XKwi_2132_lastvisit=1472282467; BDTUJIAID=b79f8f43ddce2ed3810a4307b684c454; XKwi_2132_seccode=862.64b621ed3437cbc936; XKwi_2132_ulastactivity=6bdbfiPE1XgQkwxpeN9j2GrH8GBMi%2BhPgK8u1OVBcXqlbwHugWOo; XKwi_2132_auth=c070W01fs%2BBqLUVpq2PsNBCFTtQHty%2FWzr2Qz%2Bwh57bXUUmGlKnSDGxPRAMLIUp7%2BjQZ1pXNNjpPL%2FLwq6xAB4yQJKI; XKwi_2132_lip=221.2.164.39%2C1472286930; XKwi_2132_sendmail=1; tjpctrl=1472290975670; XKwi_2132_st_t=385935%7C1472289215%7C83d7492025641aedea0cb994ded4b05a; XKwi_2132_atarget=1; XKwi_2132_forum_lastvisit=D_64_1472289215; XKwi_2132_visitedfid=47D64D45; XKwi_2132_st_p=385935%7C1472289261%7C5a4db20552090db5966e6c8ffc04d125; XKwi_2132_viewid=tid_21440; XKwi_2132_smile=1D1; XKwi_2132_sid=cnWCTv; XKwi_2132_checkpm=1; Hm_lvt_3f7cd21120c10c32ab7b8cbb432fd43d=1472286068; Hm_lpvt_3f7cd21120c10c32ab7b8cbb432fd43d=1472289357; XKwi_2132_lastact=1472289357%09misc.php%09patch; XKwi_2132_connect_is_bind=0"

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
    # for s in xrange(1, random.randint(2,10)):
    #     time.sleep(1)
    #     print 'sleep'
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
	# for s in xrange(1, random.randint(2,10)):
        #     time.sleep(1)
        #     print 'sleep'
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
        authors = soup3.findAll(attrs={'class':'info_r_t'})
        posts_contents = soup3.findAll(attrs={'class': 't_f'})
        # 以下循环将正文部分处理成一整个字符串形式
        i = 1
        for post_contents in posts_contents:
            try:
                author = authors[2*(i-1)].findAll(name='div')[1].find(name='strong').find(name='a').string
                _time = compiled_time.search(str(posts[i-1])).group()
            except:
                print "ERROR:获取作者、时间信息出错！"
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
                ISOTIMEFORMAT = '%Y-%m-%d %X'
                spider_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
                hm = soup2.find(attrs = {'class':'hm ptn'})
                p_num = re.findall(r'[0-9]+', hm.text, re.I)
                p_look_num = p_num[0]
                p_rep_num = p_num[1]
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
