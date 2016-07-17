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
spiderUrl = "http://bbs.vc52.cn/forum.php?mod=forumdisplay&fid=48&orderby=dateline&filter=author&orderby=dateline&page="
# 入库存储的板块名称
board = "『网络资源』"
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
mysqldatabase = "vc52"

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
    response = urllib2.urlopen(spiderUrl + str(k))
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
    tagA = soup.findAll(name='a', attrs={'class': 's xst'})
    # 依次解析每一个帖子标题
    for title in tagA:
        # print title.string
        args = []
        arg = []
        # 从标题中提取帖子的链接，访问该链接从中解析出帖子更多信息
        href = urllib.unquote(title['href'])
        href = "http://bbs.vc52.cn/"+href
        try:
            response2 = urllib2.urlopen(href)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
        except:
            print "error, URL open failed!"
        posts = soup2.findAll(attrs={'class': 'pi'})
        posts_contents = soup2.findAll(attrs={'class': 't_f'})
        try:
            author = posts[0].contents[1].contents[0].string
            time = compiled_time.search(str(posts[1])).group()
        except:
            print "ERROR:获取作者、时间信息出错！"
            continue
        print author, time, title.string
        arg = [title.string, author, time, href]
        args.append(arg)
        # 以下循环将正文部分处理成一整个字符串形式
        i = 0
        for post_contents in posts_contents:
            if i == 1:
                break
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
