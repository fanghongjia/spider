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

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 需要爬取的板块连接（注意该链接下的帖子是按照发帖时间进行排序的，且去掉最后的数字）
spiderUrl = "http://www.52fzba.com/forum.php?mod=forumdisplay&fid=330&orderby=dateline&filter=author&orderby=dateline&page="
# 入库存储的板块名称
board = "泰拉瑞亚"
# 该板块内需要爬取的起始页号
page_start = 2
# 该板块内需要爬取的终止页号
page_end = 3
# 代理服务器
proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "52fzba"

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
Cookie = "BDTUJIAID=e584b371feec282e9ae29f8033f6c22f; ftcpvcouplet_fidx=1; PHPSESSID=kgfdu9khtld4pctmar34m8l4p3; tjpctrl=1469098444637; qwJR_2132_saltkey=V4evRnkp; qwJR_2132_lastvisit=1469093172; qwJR_2132_sendmail=1; qwJR_2132_ulastactivity=058cPZAp1orfLycUz8uD8%2FTXeLp0LavPUgCeaEQCKwIZd3JHzpRg; qwJR_2132_auth=f564gO0o7PxpBXjdtDYxE4TQGhQ5OZIjK2MBrTzHeuRwU9F5HtvdjL1zZRQIGppo4OyLnEoGUljak%2FAVESBh7KY70TI; qwJR_2132_lip=221.2.164.39%2C1469096872; qwJR_2132_security_cookiereport=f1b2qBtnxnLPzC5ykuieQyKlql54AWhGRnEamh1e0ZkAf04yYK3E; qwJR_2132_home_diymode=1; qwJR_2132_nofavfid=1; qwJR_2132_onlineusernum=2287; qwJR_2132_st_t=547490%7C1469096988%7Ce571305a23edf014aeca0fa1df7be0df; qwJR_2132_atarget=1; qwJR_2132_forum_lastvisit=D_75_1469096988; qwJR_2132_smile=4D1; qwJR_2132_st_p=547490%7C1469097015%7Ccafa802330b5b5e075c106803fc847ac; qwJR_2132_visitedfid=18D75; qwJR_2132_viewid=tid_14017; qwJR_2132_sid=Ht2aT6; _fmdata=EAE317DCC2BB11F97F2740F9EEEC52EB22954B4B23E99DBCBDE189B267BEB68485029C061FDE19A9745017D37903F8C1C76226F879C573D1; Hm_lvt_6b92a602712df3f78bca96f13da7346c=1468839783,1469008690,1469096516; Hm_lpvt_6b92a602712df3f78bca96f13da7346c=1469097016; pgv_pvi=7957838330; pgv_info=ssi=s5831412770; qwJR_2132_lastact=1469097019%09forum.php%09ajax; qwJR_2132_connect_is_bind=0"
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
    ('Cookie',Cookie),
    ('Connection','keep-alive')
    ]
# 以下两行用于设置代理，一般情况下无需使用
# proxy_handler = urllib2.ProxyHandler({'http':proxy_server})
# opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
for k in range(page_start, page_end):
    response = urllib2.urlopen(spiderUrl + str(k))
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
    tagA = soup.findAll(name='a', attrs={'class': 's xst'})
    # 依次解析每一个帖子标题
    for title in tagA:
        # 从标题中提取帖子的链接，访问该链接从中解析出帖子更多信息
        href = urllib.unquote(title['href'])
        try: 
            response2 = urllib2.urlopen(href)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
        except:
            print "bad url!"
            continue
        hidden = soup2.find(attrs={'class':'locked'})
        if(hidden != None):
            a_exist = hidden.find(name='a')
            if a_exist != None:
                doReply(href,"www.52fzba.com",Cookie)
        p_page_content = soup2.find(attrs={'class':'pg'})
        if(p_page_content != None):
            p_page_url_init = p_page_content.contents[1].get('href')[0:-8]
            p_page_end = p_page_content.find(name='span').string
            compiled_page = re.compile(r'[0-9]+')
            p_page_end = int(compiled_page.search(str(p_page_end)).group())
            print p_page_end,"!!!!!!"
        else:
            p_page_end = 1
            print "-------------------------------------"
        newItem = {} # 初始化一个新帖子字典
        flag = True # 识别是不是楼主的flag
        for l in range(1, p_page_end+1):
            for m in range(1,10):
                time.sleep(1)
                print "休息一会儿",m
            if(p_page_content != None):
                p_page_url = p_page_url_init + str(l) + '-1.html'
            else:
                p_page_url = href
            try:
                response3 = urllib2.urlopen(p_page_url)
                soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
                print p_page_url
            except:
                print p_page_url
                print "bad url!"
                continue
            author_content = soup3.findAll(attrs={'class':'readName b'})
            posts = soup3.findAll(attrs={'class': 'pi'})
            posts_contents = soup3.findAll(attrs={'class': 't_f'})
            # 以下循环将正文部分处理成一整个字符串形式
            i = 1

            for post_contents in posts_contents:
                try:
                    author = posts[2*(i-1)].contents[1].contents[0].string
                    _time = compiled_time.search(str(posts[2*(i-1)+1])).group()
                    floor = '';
                    floor = floor + str(posts[2*(i-1)+1].contents[1].contents[1].find(name = 'em'))[4:-5]
                    if(floor == ''):
                        floor = posts[2*(i-1)+1].contents[1].contents[1].string[2:]
                except:
                    print "ERROR:获取作者、时间、楼层信息出错！"
                    continue
                lines = post_contents.encode('utf-8')
                lines = re.sub('[?]', '', lines)
                lines = re.sub('<span style=["]display:none["]>[^>]+>', '', lines)
                lines = re.sub('<font class=["]jammer["]>[^>]+>', '', lines)
                lines = re.sub('<(.*?)>', '', lines)
                lines = lines.strip()
                print lines
                # 整理数据
                if floor == '沙发':
                    floor = '2'
                elif floor == '板凳':
                    floor = '3'
                elif floor == '地板':
                    floor = '4'
                if(i == 1 and flag == True):
                    first_floor = {
                        'author':author,
                        'title':title.string,
                        'floor':1,
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
                        'floor':floor,
                        'author':author
                    }
                    newItem[floor] = other_floor
                i += 1
        try:
            coll.insert(newItem)
        except:
            print "ERROR:数据库存储错误！"
print "板块 " + board + " 爬取结束！"
