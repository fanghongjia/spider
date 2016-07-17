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

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 需要爬取的板块连接（注意该链接下的帖子是按照发帖时间进行排序的，且去掉最后的数字）
spiderUrl = "http://bbs.125.la/forum.php?mod=forumdisplay&fid=125&orderby=dateline&filter=author&orderby=dateline&page="
# 入库存储的板块名称
board = "精易产品中心"
# 该板块内需要爬取的起始页号
page_start = 44
# 该板块内需要爬取的终止页号
page_end = 50
# 代理服务器
proxy_server = 'http://120.198.231.85:80'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "bbs125"

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
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
    ('Cookie','lDlk_ecc9_saltkey=S2MEXuwM; lDlk_ecc9_lastvisit=1468285925; lDlk_ecc9_nofavfid=1; lDlk_ecc9_smile=4D1; lDlk_ecc9_forum_lastvisit=D_102_1468292817D_205_1468301738D_105_1468330444D_51_1468400953; lDlk_ecc9_sendmail=1; lDlk_ecc9_nofocus_forum=1; lDlk_ecc9_seccloud=1; lDlk_ecc9_seccode=6627.d8c29851567b8f1192; lDlk_ecc9_ulastactivity=b35eroMZ3sGx9dPjdwiNImMv93JAxJJWE5ZbkbgnwXHsSLMSl%2B1B; lDlk_ecc9_auth=9000ZyGZ0%2F%2BwsukVA%2BZW1O8IPs4GF9mNfeX2ZZDcODxO8CV5CddMi8q2rCXoHz7Od51suBw5WqjFDqRpVxZgTrnGn50; lDlk_ecc9_lastcheckfeed=363083%7C1468469260; lDlk_ecc9_myrepeat_rr=R0; lDlk_ecc9_onlineusernum=3513; lDlk_ecc9_sid=ZYMK2R; lDlk_ecc9_connect_is_bind=0; Hm_lvt_fa32dadde3745af309b587b38d20ea1d=1468225610,1468248865,1468330240,1468469185; Hm_lpvt_fa32dadde3745af309b587b38d20ea1d=1468469268; tjpctrl=1468471068634; lDlk_ecc9_lastact=1468469268%09like.php%09'),
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
        # href = "http://bbs.125.la/"+href
        try: 
            response2 = urllib2.urlopen(href)
        except:
            print "bad url!"
            continue
        soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
        p_page_content = soup2.find(attrs={'class':'pg'})
        if(p_page_content != None):
            p_page_url_init = p_page_content.contents[1].get('href')[0:-1]
            p_page_end = p_page_content.find(name='span').string
            compiled_page = re.compile(r'[0-9]+')
            p_page_end = int(compiled_page.search(str(p_page_end)).group())
            # print p_page_end,"!!!!!!"
        else:
            p_page_end = 1
            print "-------------------------------------"
        newItem = {} # 初始化一个新帖子字典
        flag = True # 识别是不是楼主的flag
        for l in range(1, p_page_end+1):
            if(p_page_content != None):
                p_page_url = p_page_url_init + str(l)
            else:
                p_page_url = href
            # print p_page_url
            try:
                response3 = urllib2.urlopen(p_page_url)
            except:
                print "bad url!"
                continue
            soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
            posts = soup3.findAll(attrs={'class': 'pi'})
            posts_contents = soup3.findAll(attrs={'class': 't_f'})
            # 以下循环将正文部分处理成一整个字符串形式
            i = 1

            for post_contents in posts_contents:
                try:
                    author = posts[2*(i-1)].contents[1].contents[0].string
                    time = compiled_time.search(str(posts[2*(i-1)+1])).group()
                    floor = '';
                    floor = floor + str(posts[2*(i-1)+1].contents[1].contents[1].find(name = 'em'))
                    floor = floor[4:-5]
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
                # re.sub('img','',lines)
                # lines = lines[90:]
                lines = lines.strip()
                # args[i].append(lines.decode('utf-8').encode('utf-8'))
                print lines
                # 整理数据
                if(i == 1 and flag == True):
                    first_floor = {
                        'author':author,
                        'title':title.string,
                        'floor':1,
                        'content':lines,
                        'href':href,
                        'board':board,
                        'time':time
                    }
                    print "爬到",time,title,"了"
                    newItem['1'] = first_floor
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
