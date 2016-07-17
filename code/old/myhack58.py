# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import MySQLdb
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
spiderUrl = "http://bbs.myhack58.com/thread.php?fid-39-page-"
# 入库存储的板块名称
board = " 黑吧IT技术学习区"
# 该板块内需要爬取的起始页号
page_start = 1
# 该板块内需要爬取的终止页号
page_end = 2
# 代理服务器
proxy_server = 'http://120.198.231.85:80'
# 数据库信息
mysqlHost = "172.26.253.87"
mysqlUser = "root"
mysqlPasswd = "YUgjBN"
mysqldatabase = "myhack58"

'''
---------------------------------------------------------
'''

# 用于匹配日期的正则表达式
compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')
# 数据库的连接信息
conn = MySQLdb.connect(
    host=mysqlHost,
    user=mysqlUser,
    passwd=mysqlPasswd,
    db=mysqldatabase,
    charset="utf8")
cursor = conn.cursor()
# 设置http报文的header信息
opener = urllib2.build_opener()
opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
# 以下两行用于设置代理，一般情况下无需使用
# proxy_handler = urllib2.ProxyHandler({'http':proxy_server})
# opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
for k in range(page_start, page_end):
    response = urllib2.urlopen(spiderUrl + str(k) + ".html")
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
    tagA = soup.findAll(name = 'h3')
    for title in tagA:
        title = title.find(name = 'a')
        args = []
        arg = []
        # 从标题中提取帖子的链接，访问该链接从中解析出帖子更多信息
        href = urllib.unquote(title['href'])
        href = "http://bbs.myhack58.com/"+href
        try:
            response2 = urllib2.urlopen(href)
        except:
            print "URL open failed!"
            continue
        soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
'''

'''
        p_page_start
        p_page_end
        for l in range(p_page_start, p_page_end):
            p_page_url = ''
            try:
                respons3 = urllib2.urlopen(p_page_url)
            except:
                print "URL open failed!"
                continue
            soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
            author_content = soup3.findAll(attrs={'class':'fl black'})
            time_content = soup3.findAll(attrs={'class':'fl gray'})
            posts_contents = soup3.findAll(attrs={'class': 'tpc_content'})
            print author_content
            print time_content
            print posts_contents
            # 以下循环将正文部分处理成一整个字符串形式
            # zhu  shi   diao if jiu  ke yi pa suo  you  hui tie le 
            i = 0
            for post_contents in posts_contents:
                #if i == 1:
                #    break
                try:
                    author = author_content[i].find(name = 'a').string
                    time = compiled_time.search(str(time_content[i])).group()
                except:
                    print "ERROR:获取作者、时间信息出错！"
                    continue
                arg = [title.string, author, time, href]
                args.append(arg)
                post_contents = posts_contents[i].find(attrs={'class': 'f14'})
                lines = post_contents.encode('utf-8')
                lines = re.sub('[?]', '', lines)
                lines = re.sub('<span style=["]display:none["]>[^>]+>', '', lines)
                lines = re.sub('<font class=["]jammer["]>[^>]+>', '', lines)
                lines = re.sub('<(.*?)>', '', lines)
                # re.sub('img','',lines)
                # lines = lines[90:]
                lines = lines.strip()
                args[i].append(lines.decode('utf-8').encode('utf-8'))
                print lines
                args[i].append(board)
                i += 1
                # 将数据存入数据库的contents表
                sql = "insert into contents(title,author,time,url,contents,board) values(%s,%s,%s,%s,%s,%s)"
                try:
                    cursor.executemany(sql, args)
                except:
                    print "ERROR:数据库存储错误！"
                conn.commit()
cursor.close()
conn.close()
print "板块 " + board + " 爬取结束！"
