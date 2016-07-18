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
from doReply import doReply

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 需要爬取的板块连接（注意该链接下的帖子是按照发帖时间进行排序的，且去掉最后的数字）
spiderUrl = "http://bbs.2cto.com/thread.php?fid=94&page="
# 入库存储的板块名称
board = "评论"
# 该板块内需要爬取的起始页号
page_start = 321
# 该板块内需要爬取的终止页号
page_end = 525
# 代理服务器
proxy_server = 'http://120.198.231.85:80'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "2cto"

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
Cookie = "02b4a_cloudClientUid=53525456; 02b4a_winduser=DANWBgQCaFdXDQ4BBQRQAVcIB1AFUlMDUlwAB1JSUA4EU1VUB1RSPw; Hm_lvt_1898984a3d796e86ad73ad1f4bc9f240=1468557776,1468586892; 02b4a_readlog=%2C269951%2C269956%2C325302%2C269953%2C358419%2C152898%2C332123%2C337860%2C337872%2C318488%2C; 02b4a_ol_offset=291; 02b4a_threadlog=%2C73%2C91%2C67%2C90%2C69%2C33%2C94%2C49%2C; 02b4a_ci=thread%091468751393%09%0949; 02b4a_lastpos=other; 02b4a_lastvisit=37%091468751394%09%2Fy.php%3Factionsync%26nowtime1468751753960%26verify13289ab7"
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'),
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
    tagA = soup.findAll(name='a', attrs={'class': 'subject_t f14'})
    # 依次解析每一个帖子标题
    for title in tagA:
        # 从标题中提取帖子的链接，访问该链接从中解析出帖子更多信息
        href = urllib.unquote(title['href'])
        href = "http://bbs.2cto.com/"+href
        try: 
            response2 = urllib2.urlopen(href)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
        except:
            print "bad url!"
            continue
        hidden = soup2.find(attrs={'class':'f12 quoteTips'})
        if(hidden != None):
            doReply(href,"bbs.2cto.com",Cookie)
        p_page_content = soup2.find(name='div',attrs={'class':'pages'})
        if(p_page_content != None):
            a_content = p_page_content.findAll(name='a')
            p_page_url_init = "http://bbs.2cto.com/" + a_content[0].get('href')[0:-1]
            p_card_num = soup2.find(attrs={'id':'topicRepliesNum'}).string
            p_page_end = int(p_card_num)/10 + 1
        else:
            p_page_end = 1
        newItem = {} # 初始化一个新帖子字典
        flag = True # 识别是不是楼主的flag
        for l in range(1, p_page_end+1):
            if(p_page_content != None):
                p_page_url = p_page_url_init + str(l)
            else:
                p_page_url = href
            try:
                response3 = urllib2.urlopen(p_page_url)
                soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
            except:
                print p_page_url
                print "bad url!"
                continue
            # posts = soup3.findAll(attrs={'class': 'pi'})
            # posts_contents = soup3.findAll(attrs={'class': 't_f'})
            author_content = soup3.findAll(attrs={'class':'readName b'})
            time_content = soup3.findAll(attrs={'class':'tipTop s6'})
            floor_content = soup3.findAll(attrs={'class':'s2 b cp'})
            posts_contents = soup3.findAll(attrs={'class': 'tpc_content'})
            # 以下循环将正文部分处理成一整个字符串形式
            i = 0

            for post_contents in posts_contents:
                try:
                    author = author_content[i].contents[1].string
                    time = compiled_time.search(str(time_content[i])).group()
                    floor = str(floor_content[i].string)
                except:
                    print "ERROR:获取作者、时间、楼层信息出错！"
                    continue
                post_contents = posts_contents[i].find(attrs={'class': 'f14 mb10'})
                if(post_contents == None):    
                    continue
                lines = post_contents.encode('utf-8')
                lines = re.sub('[?]', '', lines)
                lines = re.sub('<span style=["]display:none["]>[^>]+>', '', lines)
                lines = re.sub('<font class=["]jammer["]>[^>]+>', '', lines)
                lines = re.sub('<(.*?)>', '', lines)
                # re.sub('img','',lines)
                # lines = lines[90:]
                lines = lines.strip()
                # args[i].append(lines.decode('utf-8').encode('utf-8'))
                print lines
                # 整理数据
                if(i == 0 and flag == True):
                    first_floor = {
                        'author':author,
                        'title':title.string,
                        'floor':floor,
                        'content':lines,
                        'href':href,
                        'board':board,
                        'time':time
                    }
                    print "-----------------爬到",time,title.string,"了--------------------"
                    newItem['0'] = first_floor
                    flag = False
                else:
                    other_floor = {
                        'content':lines,
                        'time':time,
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
