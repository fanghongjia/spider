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
# 爬取的网站域名
domain = "bbs.anjian.com"
# 起始tid
tid_start = 443800
# 6月30最后的tid
tid_end = 443801
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
Cookie = "pgv_pvid=8490825450; dntVC=QyG3wKFGWZBLQW8ifAC5xNteYmIvemPAt0yR00npppA=; pgv_pvi=9974319104; ASP.NET_SessionId=fg3qdanvx4r2bkvrixlvcwaa; __qc_wId=519; lastposttitle=d41d8cd98f00b204e9800998ecf8427e; lastpostmessage=b3b457cc61a9ad55f21feb2118117f2a; lastolupdate=891602063; lastposttime=2016-08-11 11:38:57; visitedforums=234,244,250,221,219,245,240,56,81,207; dnt=userid=4060473&password=5dIPmdcddfIGzNTTBinEwTZdBnDxp2V5Qo07Z8MeQ3qiAllJwJPaAA%3d%3d&tpp=0&ppp=0&pmsound=0&invisible=0&referer=showtopic.aspx%3ftopicid%3d343260%26page%3d1%26auctionpage%3d1%26forumpage%3d1&sigstatus=1&expires=43200&userinfotips=&visitedforums=244%2c221%2c250%2c234%2c245%2c56%2c219%2c233%2c66%2c240&oldtopic=D343260D543440D565244D591352D569461; dntusertips=userinfotips=%e7%a7%af%e5%88%86%3a5%2c%e7%94%a8%e6%88%b7%e7%bb%84%3a%3cfont+color%3d%22FF6500%22%3e%e6%8c%89%e9%94%ae%e7%b2%be%e7%81%b5%e4%bc%9a%e5%91%98%3c%2ffont%3e%2c%e9%b2%9c%e8%8a%b1%3a+0%e6%9c%b5%2c%e9%93%9c%e5%b8%81%3a+33%e4%b8%aa%2c%e9%93%b6%e5%b8%81%3a+0%e4%b8%aa%2c%e9%87%91%e5%b8%81%3a+0%e4%b8%aa; lastactivity=onlinetime=896047748&oltime=896047748; allowchangewidth=; AJSTAT_ok_pages=1; AJSTAT_ok_times=3; Hm_lvt_5d96b144d9b7632ed0ce359527dcc65d=1470820593,1470821337,1470821363,1470877578; Hm_lpvt_5d96b144d9b7632ed0ce359527dcc65d=1470891182"
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
    ('Cookie',Cookie),
    ('Connection','keep-alive')
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
            # doReply(href, domain, k, Cookie)
            f = open('needReply.txt','a')
            f.write(href + '    ----href bad')
            f.write('\n')
            f.close
        else:
            f = open('hidden.txt','a')
            f.write(href + '    ----href bad')
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
    p_page_end = int(math.ceil(float(p_rep_num) / 20))
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
