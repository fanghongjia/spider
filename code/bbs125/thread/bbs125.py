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
from multiprocessing.dummy import Pool as ThreadPool


reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 爬取的网站域名
domain = "bbs.125.la"
# 起始tid
tid_start = 40
# 6月30最后的tid
tid_end = 66
# 代理服务器
# proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "test"
coll_name = "bbs125_test_thread"

'''
---------------------------------------------------------
'''

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

# 用于匹配日期的正则表达式
compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')

def onespider(url):
    # 设置http报文的header信息
    opener = urllib2.build_opener()
    Cookie = "lDlk_ecc9_saltkey=ZJQz5lj0; lDlk_ecc9_lastvisit=1470395868; lDlk_ecc9_sid=A381e8; lDlk_ecc9_lastact=1470399514%09forum.php%09; lDlk_ecc9_sendmail=1; Hm_lvt_fa32dadde3745af309b587b38d20ea1d=1470399470; Hm_lpvt_fa32dadde3745af309b587b38d20ea1d=1470399516; lDlk_ecc9_ulastactivity=3b5dAWO7kvzHuDcG%2F%2Fd0zcitjHfpCrfanOQFxsz%2FHQxXAHKPO5oc; lDlk_ecc9_auth=ba27pUzFIwwrrTgeRTtK5LrL3Xen7AVwXwswIMThv5frRRAn8mSYJil8%2BnCGogg1OUJxQEKdAVkT6FYJBGrz0Qm9KxA; lDlk_ecc9_lastcheckfeed=363083%7C1470399485; lDlk_ecc9_lip=202.102.144.8%2C1470397927; lDlk_ecc9_connect_is_bind=0; lDlk_ecc9_nofavfid=1; lDlk_ecc9_onlineusernum=5782; lDlk_ecc9_myrepeat_rr=R0; lDlk_ecc9_nofocus_forum=1; tjpctrl=1470401288179; lDlk_ecc9_wx_from=8601ZdCNX8jSB%2BfVpEeMlOKbm0tFllWv27jSI4qT85hZMqN8D3r1"
    opener.addheaders = [
        ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
        ('Cookie',Cookie),
        ('Connection','keep-alive')
    ]
    urllib2.install_opener(opener)
    response2 = urllib2.urlopen(href)
    soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
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
        return
    if(p_page_content != None):
        try:
            p_page_url_init = p_page_content.find(name = 'a').get('href')[:-1]
        except:
            print "bad url!"
            f = open('badurl.txt','a')
            f.write(href + '    ----p_page_init bad')
            f.write('\n')
            f.close()
            return
        p_page_end = p_page_content.find(name='span').string
        compiled_page = re.compile(r'[0-9]+')
        p_page_end = int(compiled_page.search(str(p_page_end)).group())
        if p_page_end > 400:
            exPage(soup2, opener, coll, domain, href, p_page_end, p_page_url_init)
            return
    else:
        p_page_end = 1
    print 'this post has ', p_page_end, 'pages.'
    try:
        board = soup2.find(attrs = {'class':'bm cl'}).findAll(name = 'a')[-2].text
        title = soup2.find(attrs = {'id':'thread_subject'}).text
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(href + '    ----board or title bad')
        f.write('\n')
        f.close()
        return
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
            return
        posts = soup3.findAll(attrs={'class': 'pi'})
        posts_contents = soup3.findAll(attrs={'class': 't_f'})
        # 以下循环将正文部分处理成一整个字符串形式
        i = 1
        for post_contents in posts_contents:
            try:
                author = posts[2*(i-1)].contents[1].contents[0].string
                _time = compiled_time.search(str(posts[2*(i-1)+1])).group()
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
            if(i == 1 and flag == True):
                first_floor = {
                    'author':author,
                    'title':title,
                    'floor':str(floor),
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

url_num = 0
urls = []
time1 = time.time()
for k in range(tid_start, tid_end):
    href = "http://" + domain +"/thread-" + str(k) + "-1-1.html"
    urls.append(href)
    url_num += 1
    if url_num == 4:
        pool = ThreadPool(4)
        print urls
        pool.map(onespider, urls)
        pool.close()
        pool.join()
        url_num = 0
        urls = []
print "网站" + domain + " 爬取结束！"
time2 = time.time()
print 'tread-> ', str(time2 - time1)
