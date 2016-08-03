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

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 需要爬取的板块连接（注意该链接下的帖子是按照发帖时间进行排序的，且去掉最后的数字）
spiderUrl = "http://www.9iwuc.com/forum.php?mod=forumdisplay&fid=2&orderby=dateline&filter=author&orderby=dateline&page="
# 入库存储的板块名称
board = "新人社区"
# 该板块内需要爬取的起始页号
page_start = 1
# 该板块内需要爬取的终止页号
page_end = 3
# 代理服务器
proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "9iwuc"

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
Cookie = "kUgw_2132_saltkey=Y2B6f7f7; kUgw_2132_lastvisit=1469095487; _uab_collina=146909886790173929168546; kUgw_2132_ulastactivity=d865AnZoyMAXdmL4WmMoZSMAoN6YjNREoF20aTBNt6xc77BqGyGC; kUgw_2132_auth=9bffmb6zR1eCHbfC5FIUK66rbnYsyOxId1U5YM0gdbdiNXhVF9bZLJbN0uOK9eWpUytE1XEZE0MLmkvfHLQopqBg; kUgw_2132_nofavfid=1; kUgw_2132_home_readfeed=1469099176; tjpctrl=1469100756567; kUgw_2132_pc_size_c=2fdbaec; kUgw_2132_connect_not_sync_t=1; kUgw_2132_visitedfid=45D40D39; kUgw_2132_st_t=2671%7C1469099728%7Cb26ecbfe184b6d12db0c83bbb3d04c34; kUgw_2132_forum_lastvisit=D_39_1469099537D_40_1469099620D_45_1469099728; kUgw_2132_sendmail=1; kUgw_2132_checkpm=1; kUgw_2132_lastact=1469099806%09forum.php%09viewthread; kUgw_2132_connect_is_bind=0; kUgw_2132_st_p=2671%7C1469099806%7Cb8fce5f1e2a6c7544751bb6c988fb9e9; kUgw_2132_viewid=tid_18; kUgw_2132_sid=xnIDnn; kUgw_2132_smile=1D1; kUgw_2132_noticeTitle=1; _umdata=BA335E4DD2FD504F96A2511DD5D63351664B4C74DC9F52D0356162481D878590D38322107110972C700668F9A382A3D6FD4E024474DA7742C89A7C1207D0654A877A329830844C53E17171FE4CB309C854333700B7A1F54729960AB00ACC508C"
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
        href = "http://www.9iwuc.com/" + href
        try: 
            response2 = urllib2.urlopen(href)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
        except:
            print "bad url!"
            continue
        p_page_content = soup2.find(attrs={'class':'pg'})
        if(p_page_content != None):
            p_page_url_init = "http://www.9iwuc.com/" + p_page_content.contents[1].get('href')[0:-1]
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
                p_page_url = p_page_url_init + str(l)
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
