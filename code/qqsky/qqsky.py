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
domain = "bbs.qqsky.net"
# 起始tid
tid_start = 238189
# 6月30最后的tid
tid_end = 306784 #306784
# 代理服务器
# proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "qqsky"

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
Cookie = "5j0w_2132_saltkey=kShvHd9g; 5j0w_2132_lastvisit=1470816167; 5j0w_2132_sid=HHh390; 5j0w_2132_lastact=1470819820%09misc.php%09patch; 5j0w_2132_onlineusernum=4218; 5j0w_2132_sendmail=1; 5j0w_2132_ulastactivity=52a1v2DiHEYG9vQpBTnkh60uWmKrehLHAHM%2F3xeOXgHeYbbZrI0k; 5j0w_2132_auth=7727FFmg4g%2BH%2FvkplIiD08rZ4rn9Yk2oEnTzdWxI40N4KqCbtDNebtcU8FgHahgVciIjwC6mQbv2SfkCYS0tZwkpk%2BY; 5j0w_2132_lastcheckfeed=796396%7C1470819805; 5j0w_2132_checkfollow=1; 5j0w_2132_lip=221.2.164.37%2C1470819817; 5j0w_2132_security_cookiereport=2058x3vp1a9mEO8nAVXeSZPpemvAbLNTta1cEpyn7oWVaqw6xrbg; 5j0w_2132_connect_is_bind=0; 5j0w_2132_nofavfid=1; 5j0w_2132_myrepeat_rr=R0; 5j0w_2132_checkpm=1; tjpctrl=1470821617226"
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
    href = "http://" + domain + "/thread-" + str(k) + '-1-1.html'
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
            f = open('needReply.txt','a')
            f.write(href)
            f.write('\n')
            f.close
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
            p_page_url_init = p_page_content.find(name = 'a').get('href')[:-8]
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
    for l in range(1, p_page_end+1):
        if(p_page_content != None):
            p_page_url = 'http://' + domain + '/' + p_page_url_init + str(l) + '-1.html'
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
        rec = 1 #　推荐楼层的标号，防止覆盖
        for post_contents in posts_contents:
            try:
                try:
                    author = posts[2*(i-1)].contents[1].contents[0].string
                except:
                    author = (posts[2*(i-1)].text)[2:] #处理匿名的情况
                _time = compiled_time.search(str(posts[2*(i-1)+1])).group()
                floor = ''
                floor_flag = posts[2*(i-1)+1].find(name = 'strong').find(name = 'em') # 老版本根据contents有黄牌警告会出错
                if floor_flag == None:
                    floor = posts[2*(i-1)+1].find(name = 'strong').find(name = 'a').text # for card
                else:
                    floor = floor + floor_flag.text
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
            if floor == u'\r\n沙发':
                floor = '2'
            elif floor == u'\r\n板凳':
                floor = '3'
            elif floor == u'\r\n地板':
                floor = '4'
            elif floor == u'\r\n地下':
                floor = '5'
            elif floor == u'\r\n楼主':
                floor = '0'
            elif floor == u'\r\n推荐\r\n':
                floor = u'推荐' + str(rec)
                rec = rec + 1
            elif floor_flag == None and i != 1: # 对于置顶贴这种情况的处理，例:http://bbs.hitui.com/forum.php?mod=viewthread&tid=111434&extra=page%3D2%26filter%3Dauthor%26orderby%3Ddateline
                print floor
                compiled_floor = re.compile(r'[0-9]+')
                floor = compiled_floor.search(floor).group()
            if(i == 1 and flag == True):
                first_floor = {
                    'author':author,
                    'title':title,
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
        for t in range(1, int(random.randint(0,2))):
            time.sleep(1)
            print 'sleep', t, 's'
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
