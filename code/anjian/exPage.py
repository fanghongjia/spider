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

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')

def exPage(soup, opener, coll, domain, href, p_page_end, p_page_url_init, tid):
    urllib2.install_opener(opener)
    # 用于匹配日期的正则表达式
    compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    spider_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    hm = soup.find(attrs = {'class':'hm'})
    p_num = re.findall(r'[0-9]+', hm.text, re.I)
    p_look_num = p_num[0]
    p_rep_num = p_num[1]
    try:
        board = soup.find(attrs = {'id':'nav'}).findAll(name = 'a')[1].text
        title = soup.find(attrs = {'id':'nav'}).findAll(name = 'a')[2].text
    except:
        print "bad url!"
        f = open('badurl.txt','a')
        f.write(href + '    ----board or title bad')
        f.write('\n')
        f.close()
        return
    print title
    i = 1
    newItem = {} # 初始化一个新帖子字典
    flag = True # 识别是不是楼主的flag
    for l in range(1, p_page_end):
        if l == 0:
            continue
        for t in range(1, random.randint(0, 1)): 
            print 'sleep', t, 's'
            time.sleep(1)
        p_page_url = p_page_url_init + str(tid) + "-" + str(l) + ".aspx?forumpage=1&typeid=-1"
        try:
            response3 = urllib2.urlopen(p_page_url)
            soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
        except:
            print p_page_url
            print "bad url!"
            f = open('badurl.txt','a')
            f.write(p_page_url)
            f.write('\n')
            f.close()
            continue
        authors = soup3.findAll(attrs = {'class':'poster'})
        _times = soup3.findAll(attrs = {'class':'postinfo'})
        posts_contents = soup3.findAll(attrs={'class': 't_msgfont'})
        # 以下循环将正文部分处理成一整个字符串形式
        j = 1
        for post_contents in posts_contents:
            try:
                author = authors[j-1].text
                author = author.replace('\n', '')
                _time = _times[j-1].text
                _time = compiled_time.search(_time).group()
            except:
                print "ERROR:获取作者、时间出错！"
                f = open('badurl.txt', 'a')
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
                _title = title
                print "爬到",_time,title,"了"
                newItem['1'] = first_floor
                flag = False
            else:
                other_floor = {
                    'content':lines,
                    'time':_time,
                    'floor':i,
                    'author':author
                }
                newItem[str(i)] = other_floor
            if i == 1:
                try:
                    coll.insert(newItem)
                except:
                    print 'db insert wrong'
            else:
                i_str = str(i)
                try:
                    coll.update({"1.href": href}, {"$set": {i_str: other_floor}})
                except:
                    print "db update wrong"
            j += 1
            i += 1
