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
spiderUrl = "http://bbs.blackbap.org/forum.php?mod=forumdisplay&fid=33&orderby=dateline&orderby=dateline&filter=author&page="
# 入库存储的板块名称
board = "分享和下载 - Sharing & Downloads"
# 该板块内需要爬取的起始页号
page_start = 15
# 该板块内需要爬取的终止页号
page_end = 17
# 代理服务器
proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "blackbap"

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
Cookie = "B96o_2132_saltkey=ZuegE46S; B96o_2132_lastvisit=1470101431; B96o_2132_seccode=121.86bc7d56af73c2e987; B96o_2132_ulastactivity=5812%2BgKvLpALssJc%2F4oygtXC9FfPzVzEr1K%2BS0Fg6pC5ekfeAIom; B96o_2132_auth=779dXl4hxTNuKW52cry9Fpnb%2BrcQYeUbVHimfwmUG55WmqGMZJiwL7%2F9%2BWNPApHjvMLquGj%2FOLeGA%2Fqwsv9i7aYijA; B96o_2132_lastcheckfeed=11297%7C1470192983; B96o_2132_lip=202.102.144.8%2C1470144275; B96o_2132_st_p=11297%7C1470193015%7C9564b2074cda4d18f2667a94241f9819; B96o_2132_viewid=tid_8134; B96o_2132_nofavfid=1; B96o_2132_onlineusernum=338; B96o_2132_visitedfid=21D10D11D29D18; B96o_2132_st_t=11297%7C1470193134%7C9558bf09ae6e0822557429aa374107b4; B96o_2132_forum_lastvisit=D_18_1470105356D_29_1470105808D_11_1470192986D_10_1470193102D_21_1470193134; B96o_2132_smile=4D1; B96o_2132_sid=G6xvwg; B96o_2132_checkpm=1; B96o_2132_sendmail=1; B96o_2132_lastact=1470193227%09misc.php%09patch"
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
    try:
        response = urllib2.urlopen(spiderUrl + str(k))
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(spiderUrl + str(k))
        f.write('\n')
        continue
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
    tagA = soup.findAll(name='a', attrs={'class': 'xst'})
    # 依次解析每一个帖子标题
    for title in tagA:
        # 从标题中提取帖子的链接，访问该链接从中解析出帖子更多信息
        href = urllib.unquote(title['href'])
        href = 'http://bbs.blackbap.org/' + href
        try: 
            response2 = urllib2.urlopen(href)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
        except:
            print "bad url!"
            f = open('badurl.txt','a')
            f.write(href)
            f.write('\n')
            continue
        hidden = soup2.find(attrs={'class':'locked'})
        if hidden != None:
            if hidden.find(name='a') != None:
                doReply(href,'bbs.blackbap.org',Cookie)
        p_page_content = soup2.find(attrs={'class':'pg'})
        if(p_page_content != None):
            try:
                p_page_url_init = title.get('href') + '&page='
            except:
                continue
            p_page_end = p_page_content.find(name='span').string
            compiled_page = re.compile(r'[0-9]+')
            p_page_end = int(compiled_page.search(str(p_page_end)).group())
            if p_page_end > 400:
                print p_page_url
                print "too much pages!"
                f = open('badurl.txt','a')
                f.write(p_page_url + '  ---too much pages!')
                f.write('\n')
                continue
            print p_page_end,"!!!!!!"
        else:
            p_page_end = 1
            print "-------------------------------------"
        newItem = {} # 初始化一个新帖子字典
        flag = True # 识别是不是楼主的flag
        for l in range(1, p_page_end+1):
            if(p_page_content != None):
                p_page_url = "http://bbs.blackbap.org/" + p_page_url_init + str(l)
            else:
                p_page_url = href
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
            i = 1

            for post_contents in posts_contents:
                try:
                    author = posts[2*(i-1)].contents[1].contents[0].string
                    _time = compiled_time.search(str(posts[2*(i-1)+1])).group()
                    floor = '';
                    floor = floor + str(posts[2*(i-1)+1].contents[1].contents[1].find(name = 'em'))[4:-5]
                    if(floor == ''):
                        floor = posts[2*(i-1)+1].contents[1].contents[1].string[1:]
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
                elif floor == '地下室':
                    floor = '5'
                elif floor == '下水道':
                    floor = '6'
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
