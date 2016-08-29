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
domain = "bbs.anjian.com"
# 起始tid
tid_start = 600420
# 6月30最后的tid
tid_end = 629724 #629724
# 代理服务器
# proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "anjian"

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
Cookie = "onlineusercount=1430; allowchangewidth=; lastolupdate=990902268; ASP.NET_SessionId=d41qyz5zasqvi5ljnpbemxq3; __qc_wId=719; pgv_pvid=9052956240; AJSTAT_ok_pages=2; AJSTAT_ok_times=1; Hm_lvt_5d96b144d9b7632ed0ce359527dcc65d=1470986050; Hm_lpvt_5d96b144d9b7632ed0ce359527dcc65d=1470986062; reurl=http://bbs.anjian.com/login.aspx?referer=forumindex.aspx; dnt=userid=4060473&password=5dIPmdcddfIGzNTTBinEwTZdBnDxp2V5Qo07Z8MeQ3qiAllJwJPaAA%3d%3d&tpp=0&ppp=0&pmsound=0&invisible=0&referer=index.aspx&sigstatus=1&expires=43200&userinfotips=; JustLogin=firstL; dntusertips=userinfotips=%e7%a7%af%e5%88%86%3a16%2c%e7%94%a8%e6%88%b7%e7%bb%84%3a%3cfont+color%3d%22FF6500%22%3e%e6%8c%89%e9%94%ae%e7%b2%be%e7%81%b5%e4%bc%9a%e5%91%98%3c%2ffont%3e%2c%e9%b2%9c%e8%8a%b1%3a+0%e6%9c%b5%2c%e9%93%9c%e5%b8%81%3a+53%e4%b8%aa%2c%e9%93%b6%e5%b8%81%3a+0%e4%b8%aa%2c%e9%87%91%e5%b8%81%3a+0%e4%b8%aa"
opener.addheaders = [
    ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'),
    ('Cookie', Cookie),
    ('Connection', 'keep-alive'),
]
# 以下两行用于设置代理，一般情况下无需使用
# proxy_handler = urllib2.ProxyHandler({'http':proxy_server})
# opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
for k in range(tid_start, tid_end):
    href = "http://" + domain + "/showtopic-" + str(k) + '-1.aspx'
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
    hidden = soup2.find(attrs={'class':'hidestyle'})
    if hidden != None:
        if hidden.find(name='a') != None and hidden.find(name = 'a').text == u'回复':
            doReply(href, domain, k, Cookie)
        else:
            f = open('hidden.txt','a')
            f.write(href)
            f.write('\n')
            f.close
    p_page_url_init = "http://" + domain + "/showtopic-"
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    spider_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    hm = soup2.find(attrs = {'class':'hm'})
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
    p_page_end = int(int(p_rep_num) / 20) + 1
    print 'this post has ', p_page_end, 'pages.'
    if p_page_end > 200:
        exPage(soup2, opener, coll, domain, href, p_page_end, p_page_url_init, k)
        continue
    try:
        board = soup2.find(attrs = {'id':'nav'}).findAll(name = 'a')[1].text
        title = soup2.find(attrs = {'id':'nav'}).findAll(name = 'a')[2].text
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(href + '    ----board or title bad')
        f.write('\n')
        f.close()
        continue
    newItem = {} # 初始化一个新帖子字典
    flag = True # 识别是不是楼主的flag
    j = 1 # floor flag
    for l in range(1, p_page_end+1):
        for t in range(1, random.randint(1, 3)): 
            print 'sleep', t, 's'
            time.sleep(1)
        p_page_url = p_page_url_init + str(k) + "-" + str(l) + ".aspx?forumpage=1&typeid=-1"
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
        authors = soup3.findAll(attrs = {'class':'poster'})
        _times = soup3.findAll(attrs = {'class':'postinfo'})
        posts_contents = soup3.findAll(attrs={'class': 't_msgfont'})
        # 以下循环将正文部分处理成一整个字符串形式
        i = 1 # one page floor flag
        for post_contents in posts_contents:
            try:
                author = authors[i-1].text
                author = author.replace('\n', '')
                _time = _times[i-1].text
                _time = compiled_time.search(_time).group()
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
                first_floor = {
                    'author':author,
                    'title':title,
                    'floor':i,
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
                    'floor':j,
                    'author':author
                }
                newItem[str(j)] = other_floor
            i += 1
            j += 1
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
