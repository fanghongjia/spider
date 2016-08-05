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

def exPage(soup, opener, coll, domain, board, href, p_page_end, p_page_url_init):
    urllib2.install_opener(opener)
    # 用于匹配日期的正则表达式
    compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')
    title = soup.find(attrs={'id':'thread_subject'}).string
    print title
    i = 1
    newItem = {} # 初始化一个新帖子字典
    flag = True # 识别是不是楼主的flag
    for l in range(1, p_page_end):
        if l == 0:
            continue
        p_page_url = "http://" + domain +"/" + p_page_url_init + str(l)
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
        posts = soup3.findAll(attrs={'class': 'pi'})
        posts_contents = soup3.findAll(attrs={'class': 't_f'})
        # 以下循环将正文部分处理成一整个字符串形式
        j = 1
        rec = 1 # 推荐楼层的标号，防止覆盖
        for post_contents in posts_contents:
            try:
                author = posts[2*(j-1)].contents[1].contents[0].string
                _time = compiled_time.search(str(posts[2*(j-1)+1])).group()
                floor = '';
                floor_flag = posts[2*(i-1)+1].contents[1].find(name = 'em')
                if floor_flag == None:
                    floor = posts[2*(i-1)+1].find(name = 'a').text
                else:
                    floor = floor + floor_flag.text
            except:
                print "ERROR:获取作者、时间、楼层出错！"
                f = open('badurl.txt', 'a')
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
                _title = title.string
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
