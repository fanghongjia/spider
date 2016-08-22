# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import time
import sys
import random
reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
##
# ifReply
# Description: 回复帖子
# url: 帖子首页的链接
# domian: 网站的域名，例：bbs.2cto.com
# tid: 帖子的id
# Cookie: 登录所获取的Cookie字符串
##
def doReply(url, domain, tid, Cookie):
    # 设置http报文的header信息
    opener = urllib2.build_opener()
    opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'),
            ('Cookie', Cookie),
            ('Connection', 'keep-alive'),
           ]
    urllib2.install_opener(opener)
    replys = [
        '6666666666666666666',
        'I%20want%20to%20look%20what%20locked%20by%20louzhu.',
        'There%20looking%20like%20exist%20something%20intersting.',
        'learn%20something%20from%20this%20post.',
        'Let%20me%20see%20what%20lz%20locked!',
        '%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B%E7%9C%8B',
        '%E7%9C%8B%E7%9C%8B%E6%A5%BC%E4%B8%BB%E9%9A%90%E8%97%8F%E4%BA%86%E4%BB%80%E4%B9%88',
        '%E7%9C%8B%E7%9C%8B%E5%AD%A6%E4%B9%A0%E4%B8%80%E4%B8%8B',
        '%E5%AD%A6%E4%B9%A0%E5%AD%A6%E4%B9%A0%E5%AD%A6%E4%B9%A0',
        '%E5%AD%A6%E4%B9%A0%E4%B8%8B%E5%95%8A%E5%AD%A6%E4%B9%A0',
        '%E5%AD%A6%E4%B9%A0%E5%AD%A6%E4%B9%A0%E3%80%82%E3%80%82',
        '%E6%9D%A5%E5%AD%A6%E4%B9%A0%EF%BC%8C%E7%9C%8B%E7%9C%8B',
        '%E5%9B%9E%E5%A4%8D%E7%9C%8B%E7%9C%8B%20%E6%9C%89%E7%94%A8%E4%B8%8D',
        'Good!!!!!!!!',
        '%E6%A5%BC%E4%B8%BB%E8%BE%9B%E8%8B%A6%E4%BA%86%E9%80%81%E8%8A%B1',
        '%E6%88%91%E6%9D%A5%E7%9C%8B%E7%9C%8B%E5%AD%A6%E4%B9%A0',
        '%E7%9C%8B%E7%9C%8B%E6%80%8E%E4%B9%88%E6%A0%B7',
        '%E5%A5%BD%E5%A5%BD%E5%AD%A6%E4%B9%A0',
        '%E5%AD%A6%E4%B9%A0%E4%B8%80%E4%B8%8B%E3%80%82%E5%AD%A6%E4%B9%A0%E4%B8%80%E4%B8%8B%E3%80%82',
        '%E5%AD%A6%E4%B9%A0%E5%AD%A6%E4%B9%A0~~~~~~~~~~~~~~~~~~~~~~~~'
    ]
    reply = replys[random.randint(0, 19)]
    # http://bbs.anjian.com/tools/ajax.aspx?topicid=536869&postid=0&postreplynotice=true&t=quickreply
    form_action = "http://" + domain + "/tools/ajax.aspx?topicid=" + str(tid) + "&postid=0&postreplynotice=true&t=quickreply" # 找到表单提交的地址，即处理页地址
    form_headers = {
        'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Cookie':Cookie,
        'Connection':'keep-alive',
        'Origin': 'http://bbs.anjian.com',
        'Accept': '*/*',
        'Referer': url,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    form_data = "BTitle2=&postlayer=-1&postid=0&handlekey=&usesig=1&emailnotify=on&postreplynotice=on&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&Char3=" + reply + "&replysubmit="
    request2 = urllib2.Request(form_action, form_data, form_headers)  # 往处理页发请求
    response2 = urllib2.urlopen(request2)
    # soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
    for i in range(1, 6):
        time.sleep(1)
        print "因回复而延时", i, "秒"
    return
