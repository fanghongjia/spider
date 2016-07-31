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
spiderUrl = "http://bbs.im520.com/forum.php?mod=forumdisplay&fid=34&orderby=dateline&filter=author&orderby=dateline&page="
# 入库存储的板块名称
board = "〖QQHelper系列〗 "
# 该板块内需要爬取的起始页号
page_start = 1
# 该板块内需要爬取的终止页号
page_end = 7
# 代理服务器
proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "im520"

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
Cookie = "VJ8y_2132_saltkey=HGX3y3s1; VJ8y_2132_lastvisit=1469099336; VJ8y_2132_widthauto=-1; VJ8y_2132_nofavfid=1; VJ8y_2132_auth=4c35O%2F1t%2FJJl47mf9A1%2FXiR9r%2BJJu5WZhLugRl1VNtkydtUWgFkOBS6yoOZUFL6nFhPm%2BvMPhYufvEg%2FldfpqcWvusM; VJ8y_2132_lastcheckfeed=100124%7C1469795282; VJ8y_2132_ulastactivity=19be1NwPZur%2FcGUrEOJ7U4gqho6%2FIVCXoa6EyvgTi%2F9Ih8H0LlxM; VJ8y_2132_adclose_995=1; VJ8y_2132_visitedfid=15D157D73D189D19D23D133D8D41D36; VJ8y_2132_lastact=1469864228%09forum.php%09forumdisplay; VJ8y_2132_forum_lastvisit=D_53_1469193473D_171_1469193768D_77_1469194165D_163_1469195772D_103_1469195824D_4_1469195850D_165_1469195920D_174_1469195929D_89_1469195953D_49_1469195978D_13_1469195988D_146_1469196768D_144_1469255020D_36_1469255406D_41_1469255452D_8_1469255844D_133_1469446607D_23_1469447558D_19_1469450994D_189_1469451010D_73_1469451153D_157_1469795285D_15_1469864228; VJ8y_2132_sid=S6R53r; Hm_lvt_e70b0b6205f2208b96f42b05fcde8ef0=1469253091,1469446297,1469795260,1469864171; Hm_lpvt_e70b0b6205f2208b96f42b05fcde8ef0=1469864229; VJ8y_2132_smile=1D1"
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
        href = 'http://bbs.im520.com/' + href
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
                doReply(href,'bbs.im520.com',Cookie)
        p_page_content = soup2.find(attrs={'class':'pg'})
        if(p_page_content != None):
            try:
                p_page_url_init = p_page_content.contents[1].get('href')[0:-8]
            except:
                continue
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
            if(p_page_content != None):
                p_page_url = "http://bbs.im520.com/" + p_page_url_init + str(l) + "-1.html"
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
