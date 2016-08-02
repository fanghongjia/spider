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

main_url = 'http://bbs.im520.com/forum.php?mod=viewthread&tid=547965&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26orderby%3Ddateline' #帖子首页链接

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "im520"

# 用于匹配日期的正则表达式
compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

# 设置http报文的header信息
opener = urllib2.build_opener()
Cookie = "VJ8y_2132_widthauto=-1; VJ8y_2132_saltkey=Qug4QW7W; VJ8y_2132_lastvisit=1470011710; VJ8y_2132_nofavfid=1; VJ8y_2132_adclose_995=1; VJ8y_2132_ulastactivity=6384OYHBC1yK2Kh2vSW1KazLm%2BOSNzDaVcYTzwc1nYmwOOnzPF92; VJ8y_2132_auth=2a111RUTw197G1HVYpGvGToZgCZJSa6pA6F6c78Jd0HIvfYq8pBXeHu%2FsOLaWyRySbX28%2BzuUK7d5iCvGlH3stxrFNg; VJ8y_2132_lastcheckfeed=100124%7C1470101062; VJ8y_2132_visitedfid=157D13D15; VJ8y_2132_forum_lastvisit=D_15_1470039646D_157_1470101089; VJ8y_2132_smile=1D1; VJ8y_2132_viewid=tid_547965; VJ8y_2132_sid=DHd7aM; VJ8y_2132_sendmail=1; VJ8y_2132_lastact=1470101359%09home.php%09spacecp; Hm_lvt_e70b0b6205f2208b96f42b05fcde8ef0=1469864171,1469949252,1470013882,1470101048; Hm_lpvt_e70b0b6205f2208b96f42b05fcde8ef0=1470101360"
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
    ('Cookie',Cookie),
    ('Connection','keep-alive')
]
urllib2.install_opener(opener)
board = '〖游戏大厅〗'
try:
    response2 = urllib2.urlopen(main_url)
    soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
except:
    print "bad url!"
    f = open('badurl.txt','a')
    f.write(href)
    f.write('\n')
title = soup2.find(attrs={'id':'thread_subject'}).string
print title
hidden = soup2.find(attrs={'class':'locked'})
if hidden != None:
    if hidden.find(name='a') != None:
        doReply(href,'bbs.im520.com',Cookie)
p_page_content = soup2.find(attrs={'class':'pg'})
if(p_page_content != None):
    try:
        p_page_url_init = p_page_content.contents[1].get('href')[0:-1]
    except:
        print "bad!"
p_page_end = p_page_content.find(name='span').string
compiled_page = re.compile(r'[0-9]+')
p_page_end = int(compiled_page.search(str(p_page_end)).group())
dev = int(math.ceil(p_page_end / 100))
_title = ''
i = 1
for d in range(0, dev):
    newItem = {} # 初始化一个新帖子字典
    flag = True # 识别是不是楼主的flag
    for l in range(d*100, (d+1)*100):
        if l == 0:
            continue
        if(p_page_content != None):
            p_page_url = "http://bbs.im520.com/" + p_page_url_init + str(l)
        else:
            continue
        try:
            response3 = urllib2.urlopen(p_page_url)
            soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
            print p_page_url
        except:
            print p_page_url
            print "bad url!"
            f = open('badurl.txt','a')
            f.write(p_page_url)
            f.write('\n')
            continue
        posts = soup3.findAll(attrs={'class': 'pi'})
        posts_contents = soup3.findAll(attrs={'class': 't_f'})
        # 以下循环将正文部分处理成一整个字符串形式
        j = 1
        for post_contents in posts_contents:
            try:
                author = posts[2*(j-1)].contents[1].contents[0].string
                _time = compiled_time.search(str(posts[2*(j-1)+1])).group()
                floor = '';
                floor = floor + str(posts[2*(j-1)+1].contents[1].contents[1].find(name = 'em'))[4:-5]
                if(floor == ''):
                    floor = posts[2*(j-1)+1].contents[1].contents[1].string[2:]
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
                    'href':main_url,
                    'board':board,
                    'time':_time
                }
                _title = title.string
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
                if d != 0:
                    i_str = str(i)
                    try:
                        coll.update({"1.title": _title}, {"$set": {i_str: other_floor}})
                        print "db correct"
                    except:
                        print "db wrong"
            j += 1
            i += 1
    try:
        if d == 0:
            coll.insert(newItem) 
    except:
        print "ERROR:数据库存储错误！"
