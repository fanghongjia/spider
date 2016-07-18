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
spiderUrl = "http://www.52fzba.com/forum.php?mod=forumdisplay&fid=329&orderby=dateline&orderby=dateline&filter=author&page="
# 入库存储的板块名称
board = "使命召唤"
# 该板块内需要爬取的起始页号
page_start = 1
# 该板块内需要爬取的终止页号
page_end = 2
# 代理服务器
proxy_server = 'http://120.198.231.85:80'
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
Cookie = "qwJR_2132_saltkey=aXSGroGx; qwJR_2132_lastvisit=1468836181; BDTUJIAID=e584b371feec282e9ae29f8033f6c22f; qwJR_2132_ulastactivity=311a6x%2F3bT9J5GZ0JoZCGYiyyPuA0t5kAqfn%2FpDYbALNDjQ5p6xS; qwJR_2132_auth=fb34AdR7wwvp2AVx%2BanHMkHSrLReSMcsNDA3BeyaUAQfP25mLdvzaRgdIwKxbBSNVMvLHVRwpBd77LBfhHVcVVQuXeA; qwJR_2132_lastcheckfeed=544485%7C1468839803; qwJR_2132_lip=202.102.144.8%2C1468817386; PHPSESSID=e1clbisbu76og2dedrguf2oo36; qwJR_2132_security_cookiereport=d751tMRX2dMhxGiuzmAnCTg6p77CEFqIuFtqlxsVx1%2FwOKpj3%2FkP; qwJR_2132_nofavfid=1; qwJR_2132_atarget=1; tjpctrl=1468841663330; qwJR_2132_visitedfid=17D75; qwJR_2132_st_t=544485%7C1468839930%7C991eea6826c487aac209d3c7970503df; qwJR_2132_forum_lastvisit=D_75_1468839860D_17_1468839930; qwJR_2132_st_p=544485%7C1468840130%7Ccc26e60b767e1046ca3b4ccd600ce527; qwJR_2132_viewid=tid_7220415; qwJR_2132_sid=BpD4te; qwJR_2132_sendmail=1; qwJR_2132_lastact=1468840141%09home.php%09spacecp; qwJR_2132_connect_is_bind=0; Hm_lvt_6b92a602712df3f78bca96f13da7346c=1468839783; Hm_lpvt_6b92a602712df3f78bca96f13da7346c=1468840142; pgv_pvi=7957838330; pgv_info=ssi=s2689145949; qwJR_2132_noticeTitle=1; qwJR_2132_smile=4D1; _fmdata=EAE317DCC2BB11F97F2740F9EEEC52EB22954B4B23E99DBCBDE189B267BEB68485029C061FDE19A9745017D37903F8C1C76226F879C573D1"
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
    ('Cookie',Cookie),
    ('Connection','keep-alive')
    ]
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
                    time = compiled_time.search(str(posts[2*(i-1)+1])).group()
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
