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
domain = "bbs.im520.com"
# 需要爬取的板块连接（注意该链接下的帖子是按照发帖时间进行排序的，且去掉最后的数字）
spiderUrl = "http://bbs.im520.com/forum.php?mod=forumdisplay&fid=49&orderby=dateline&filter=author&orderby=dateline&page="
# 入库存储的板块名称
board = "〖坛币交流〗"
# 该板块内需要爬取的起始页号
page_start = 395
# 该板块内需要爬取的终止页号
page_end = 510
# 代理服务器
# proxy_server = 'http://121.9.221.188'
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
Cookie = "VJ8y_2132_widthauto=-1; VJ8y_2132_saltkey=Qug4QW7W; VJ8y_2132_lastvisit=1470011710; VJ8y_2132_nofavfid=1; VJ8y_2132_auth=2a111RUTw197G1HVYpGvGToZgCZJSa6pA6F6c78Jd0HIvfYq8pBXeHu%2FsOLaWyRySbX28%2BzuUK7d5iCvGlH3stxrFNg; VJ8y_2132_lastcheckfeed=100124%7C1470101062; VJ8y_2132_ulastactivity=246b%2BdTxTvy%2BLFV98uvlkenibEZcmlOo052kKAaWa0wzICejO%2BEE; VJ8y_2132_adclose_995=1; VJ8y_2132_visitedfid=49D174D81D157D13D15; VJ8y_2132_sendmail=1; VJ8y_2132_forum_lastvisit=D_15_1470039646D_157_1470102263D_81_1470375489D_174_1470375522D_49_1470375745; VJ8y_2132_smile=1D1; VJ8y_2132_viewid=tid_547039; VJ8y_2132_lastact=1470375760%09forum.php%09; VJ8y_2132_onlineusernum=1209; VJ8y_2132_sid=ABHorJ; Hm_lvt_e70b0b6205f2208b96f42b05fcde8ef0=1470013882,1470101048,1470215254,1470375371; Hm_lpvt_e70b0b6205f2208b96f42b05fcde8ef0=1470375761"
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
        f.write(spiderUrl + str(k) + '    ----板块页面bad')
        f.write('\n')
        f.close()
        continue
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
    tagA = soup.findAll(name='a', attrs={'class': 'xst'})
    # 依次解析每一个帖子标题
    for title in tagA:
        # 从标题中提取帖子的链接，访问该链接从中解析出帖子更多信息
        href = urllib.unquote(title['href'])
        href = 'http://'+ domain + '/' + href
        try: 
            response2 = urllib2.urlopen(href)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
        except:
            print "bad url!"
            f = open('badurl.txt','a')
            f.write(href + '    ----帖子链接bad')
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
            f.write(href + '    ----页面不存在或无权访问')
            f.write('\n')
            f.close()
            continue
        if(p_page_content != None):
            try:
                p_page_url_init = title.get('href') + '&page='
            except:
                print "bad url!"
                f = open('badurl.txt','a')
                f.write(href + '    ----p_page_init出错')
                f.write('\n')
                f.close()
                continue
            p_page_end = p_page_content.find(name='span').string
            compiled_page = re.compile(r'[0-9]+')
            p_page_end = int(compiled_page.search(str(p_page_end)).group())
            print 'this post has ', p_page_end, 'pages.'
            if p_page_end > 400:
                exPage(soup2, opener, coll, domain, board, href, p_page_end, p_page_url_init)
                continue
        else:
            p_page_end = 1
        newItem = {} # 初始化一个新帖子字典
        flag = True # 识别是不是楼主的flag
        for l in range(1, p_page_end+1):
            if(p_page_content != None):
                p_page_url = "http://" + domain + "/" + p_page_url_init + str(l)
            else:
                p_page_url = href
            try:
                response3 = urllib2.urlopen(p_page_url)
                soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
                print 'located at ' + p_page_url
            except:
                f = open('badurl.txt','a')
                f.write(p_page_url + '    ----贴内页bad')
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
                    author = posts[2*(i-1)].contents[1].contents[0].string
                    _time = compiled_time.search(str(posts[2*(i-1)+1])).group()
                    floor = ''
                    floor_flag = posts[2*(i-1)+1].contents[1].find(name = 'em')
                    if floor_flag == None:
                        floor = posts[2*(i-1)+1].find(name = 'a').text
                    else:
                        floor = floor + floor_flag.text
                except:
                    print "ERROR:获取作者、时间、楼层信息出错！"
                    f = open('badurl.txt','a')
                    f.write(p_page_url + '    ----作者、时间、楼层bad')
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
                if floor == u'\r\n楼主软沙发':
                    floor = '2'
                elif floor == u'\r\n楼主硬板床':
                    floor = '3'
                elif floor == u'\r\n软地毯':
                    floor = '4'
                elif floor == u'\r\n硬地板':
                    floor = '5'
                elif floor == u'\r\n推荐\r\n':
                    floor = u'推荐' + str(rec)
                    rec = rec + 1
                elif floor_flag == None and i != 1: # 对于置顶贴这种情况的处理，例:http://bbs.hitui.com/forum.php?mod=viewthread&tid=111434&extra=page%3D2%26filter%3Dauthor%26orderby%3Ddateline
                    compiled_floor = re.compile(r'[0-9]+')
                    floor = compiled_floor.search(floor).group()
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
            if not newItem:
                print "bad url!"
                f = open('badurl.txt','a')
                f.write(href + '    ----字典为空')
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
print "板块 " + board + " 爬取结束！"
