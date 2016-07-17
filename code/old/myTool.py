# coding:utf-8
import urllib
import urllib2
import bs4
from bs4 import BeautifulSoup
import re
import MySQLdb
import cookielib

def myTool(href, title, board, cursor, conn):
    posturl = 'http://bbs.myhack58.com/login.php?'
    compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+')
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    }

    postData = {
        'lgt':'0',
        'pwuser':'wtfa',
        'pwpwd':'k1234567890',
        'question':'0',
        'customquest':'',
        'answer':'',
        'hideid':'0',
        'forward':'',
        'jumpurl':href,
        'step':'2',
        'cktime':'31536000'
    }
    print href
    postData = urllib.urlencode(postData)
    request = urllib2.Request(posturl, postData, headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
    # print soup
    author_content = soup.find(attrs={'class':'fl black'})
    time_content = soup.find(attrs={'class':'fl gray'})
    posts_contents = soup.findAll(attrs={'class': 'tpc_content'})
    try:
        author = author_content.find(name = 'a').string
        time = compiled_time.search(str(time_content)).group()
        print author,time
    except:
        print "ERROR"
        return
    args = []
    arg = []
    arg = [title.string, author, time, href]
    args.append(arg)
    # 以下循环将正文部分处理成一整个字符串形式
    i = 0
    for post_contents in posts_contents:
        if i == 1:
           break
        post_contents = post_contents.find(attrs={'class': 'f14'})
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
