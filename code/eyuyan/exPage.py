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

def exPage(soup, opener, coll, domain, href, p_page_end, p_page_url_init):
    urllib2.install_opener(opener)
    # 用于匹配日期的正则表达式
    compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')
    _map = soup.find(name = 'dibv', attrs={'id':'breadCrumb'}).find(name = a)
    board = _map[1].text
    title = _map[2].text
    p_look_content = soup.find(name ='div', attrs={'class':'readNum'})
    p_look_ems = p_look_content.findAll(name = 'em')
    p_page_content = soup.find(name='div',attrs = {'class':'pages'})
    p_card_num = p_look_ems[1].text # 回帖数
    p_look_num = p_page_ems[0].text # 阅读数
    i = 0
    newItem = {} # 初始化一个新帖子字典
    flag = True # 识别是不是楼主的flag
    for l in range(1, p_page_end+1):
        if(p_page_content != None):
            p_page_url = p_page_url_init + str(l)
        else:
            p_page_url = href
        try:
            response2 = urllib2.urlopen(p_page_url)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
            print 'located at ' + p_page_url
        except:
            print p_page_url + '   ---sub href bad'
            f = open('badurl.txt','a')
            f.write(p_page_url + '    ----sub href bad')
            f.write('\n')
            f.close()
            continue
        author_content = soup2.findAll(attrs={'class':'readName b'})
        time_content = soup2.findAll(attrs={'class':'tipTop s6'})
        floor_content = soup2.findAll(attrs={'class':'s2 b cp'})
        posts_contents = soup2.findAll(attrs={'class': 'tpc_content'})
        # 以下循环将正文部分处理成一整个字符串形式
        i = 0
        for post_contents in posts_contents:
            try:
                author = author_content[i].contents[1].string
                time = compiled_time.search(str(time_content[i])).group()
                floor = str(floor_content[i].string)
            except:
                print "ERROR:author or time or floor err"
                f = open('badurl.txt','a')
                f.write(p_page_url + '    ----author or time or floor bad')
                f.write('\n')
                f.close()
                continue
            post_contents = posts_contents[i].find(attrs={'class': 'f14 mb10'})
            if(post_contents == None): 
                print "ERROR:post_contents null"
                f = open('badurl.txt','a')
                f.write(p_page_url + '    ----post_contents null')
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
            ISOTIMEFORMAT = '%Y-%m-%d %X'
            spider_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
            if floor == u'楼主':
                floor = '0'
            elif floor == u'沙发':
                floor = '1'
            elif floor == u'板凳':
                floor = '2'
            elif floor == u'地板':
                floor = '3'
            try:
                floor_try = int(floor)
            except: 
                print "spesific floor"
                f = open('badurl.txt','a')
                f.write(p_page_url + '    ----spesific floor')
                f.write('\n')
                f.close()
                continue               
            # 整理数据
            if(i == 0 and flag == True):
                first_floor = {
                    'author':author,
                    'title':title.string,
                    'floor':floor,
                    'content':lines,
                    'href':href,
                    'board':board,
                    'time':time,
                    'ViewCount':p_look_num,
                    'ResCount':p_card_num,
                    'GmtDate':spider_time
                }
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
            if i == 0:
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
            i += 1
