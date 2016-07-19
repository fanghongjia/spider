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
spiderUrl = "http://www.kali.org.cn/forum.php?mod=forumdisplay&fid=62&orderby=dateline&filter=author&orderby=dateline&page="
# 入库存储的板块名称
board = "Nessus"
# 该板块内需要爬取的起始页号
page_start = 1
# 该板块内需要爬取的终止页号
page_end = 3
# 代理服务器
proxy_server = 'http://120.198.231.85:80'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "kali"

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
Cookie = "9f9q_746b_saltkey=HCqR667Z; 9f9q_746b_lastvisit=1468919730; 9f9q_746b_atarget=1; 9f9q_746b_seccloud=1; 9f9q_746b_sendmail=1; 9f9q_746b_st_t=0%7C1468923444%7C9df7fc7502fe671e43c50dca5d9446dc; 9f9q_746b_forum_lastvisit=D_68_1468923340D_62_1468923444; 9f9q_746b_visitedfid=62D68; 9f9q_746b_ulastactivity=1468923512%7C0; 9f9q_746b_auth=bdc5b0qwSFW5Y504Vs%2FVO%2BDCMPw2ZXTW3nT8gbksVAcmQnUvAuUyXYoNGBgyd%2FVZGfIxJ5VNbqfn%2Bj4h0RGCdnedZX0; 9f9q_746b_lastcheckfeed=432041%7C1468923512; 9f9q_746b_checkfollow=1; 9f9q_746b_lip=221.2.164.39%2C1468923512; 9f9q_746b_security_cookiereport=42dekU77BXffFvzug1ewrp%2BEYQipxG2MDfGVen%2BJ9Psj7XCW2rPR; 9f9q_746b_st_p=432041%7C1468923516%7C1e0909d1ca9d7d16c9b90cfdf816855e; 9f9q_746b_viewid=tid_17260; Hm_lvt_cb48ed518253dd6c5988e6eaa2af309e=1468923335; Hm_lpvt_cb48ed518253dd6c5988e6eaa2af309e=1468923518; 9f9q_746b_checkpm=1; CNZZDATA1256836065=1065794573-1468920054-%7C1468920054; 9f9q_746b_seccode=819.66918967cba3ed32a9; Hm_lvt_2ba792dbf616f4e6810c53e2e602df55=1468923335; Hm_lpvt_2ba792dbf616f4e6810c53e2e602df55=1468923518; 9f9q_746b_lastact=1468923516%09plugin.php%09; 9f9q_746b_connect_is_bind=0; 9f9q_746b_dcaptchasig=h01539435bbb49b3c9a63a5ffe2fde33cf3d68a29cdd256239589e29c7289c7cfcc53f2cb68d5ac02acfa86bb085805402b7aa278ce811a3baadbc98befe85e77d2; tjpctrl=1468925320034"
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
