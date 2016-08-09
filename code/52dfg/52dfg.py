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
domain = "www.52dfg.com"
# 起始tid
tid_start = 76119
# 6月30最后的tid
tid_end = 76120 #6.30 -> 77786
# 代理服务器
# proxy_server = 'http://121.9.221.188'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "52dfg"

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
Cookie = "__cfduid=d81036d2a081d7e9dd5c92175cb34c1cb1470711463; WBzh_2132_saltkey=W2F2recx; WBzh_2132_lastvisit=1470707554; BDTUJIAID=0cd85c52c8ff3cf2d2580cd73ca05d60; bdshare_firstime=1470711481044; WBzh_2132_ulastactivity=3c80QqEPzYALDJvGGxbpHASeIFr6hlElKPOsBEnjinb4xgPkFDCS; WBzh_2132_auth=7b924knKg0C1a0zuN9vvZF86aE6BtoRjdLFPH8ZSloQeQUBL5zQmEt89ETkrV6OHA9aE87HGVlnfFUeyyVa739%2BXIxQ; WBzh_2132_nofavfid=1; WBzh_2132_atarget=1; WBzh_2132_lip=221.2.164.39%2C1470712287; tjpctrl=1470716519747; WBzh_2132_resendemail=1470714420; WBzh_2132_st_t=363692%7C1470714781%7C3cd15b2521b715f96f3476bb05f962d8; WBzh_2132_forum_lastvisit=D_43_1470711398D_75_1470711423D_41_1470714617D_42_1470714643D_40_1470714781; WBzh_2132_visitedfid=40D42D91D41D75D43D2; WBzh_2132_connect_not_sync_t=1; WBzh_2132_st_p=363692%7C1470715190%7Cb5f03abbd29f980196190c9a44c72ddc; WBzh_2132_viewid=tid_72644; WBzh_2132_check_key=; WBzh_2132_check_address=; WBzh_2132_smile=4D1; WBzh_2132_sid=m889N0; Hm_lvt_d88cea092cb57b6e589d21dfb8700b5e=1470711464; Hm_lpvt_d88cea092cb57b6e589d21dfb8700b5e=1470715777; CNZZDATA1255557630=813320789-1470707322-%7C1470712732; WBzh_2132_connect_is_bind=0; WBzh_2132_lastact=1470715468%09like.php%09"
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
    href = "http://" + domain +"/thread-" + str(k) + "-1-1.html"
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
            if hidden.find(name = 'a').text == u'回复':
                doReply(href, domain, Cookie)
            else:
                f = open('needPayUrl.txt','a')
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
            p_page_url_init = "http://" + domain + "/thread-"
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
            exPage(soup2, opener, coll, domain, href, p_page_end, p_page_url_init, k)
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
            p_page_url = p_page_url_init + str(l) + "-1-" + str(k) + ".html"
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
                author = posts[2*(i-1)].contents[1].contents[0].string
                _time = compiled_time.search(str(posts[2*(i-1)+1])).group()
                floor = ''
                floor_flag = posts[2*(i-1)+1].find(name = 'strong').find(name = 'em') # 老版本根据contents有黄牌警告会出错
                if floor_flag == None:
                    floor = posts[2*(i-1)+1].find(name = 'strong').find(name = 'a').text
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
            elif floor == u'\r\n楼主':
                floor = '0'
            elif floor == u'\r\n推荐\r\n':
                floor = u'推荐' + str(rec)
                rec = rec + 1
            elif floor_flag == None and i != 1: # 对于置顶贴这种情况的处理，例:http://bbs.hitui.com/forum.php?mod=viewthread&tid=111434&extra=page%3D2%26filter%3Dauthor%26orderby%3Ddateline
                compiled_floor = re.compile(r'[0-9]+')
                floor = compiled_floor.search(floor).group()
            if(i == 1 and flag == True):
                first_floor = {
                    'author':author,
                    'title':title,
                    'floor':'1',
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
