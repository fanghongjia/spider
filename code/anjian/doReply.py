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
# Cookie: 登录所获取的Cookie字符串
##
def doReply(url, domain, tid, Cookie):
    # 设置http报文的header信息
    opener = urllib2.build_opener()
    opener.addheaders = [
            ('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'),
            ('Cookie',Cookie),
            ('Connection','keep-alive')
        ]
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url) #打开这个帖子
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8") #解析这个帖子
    form = soup.find(attrs = {'id':'quickpostform'}) # 找到表单
    if form == None:
        return
    hiddens = form.findAll(attrs={'type':'hidden'}) # 找到表单内的隐藏域
    form_data = {} # 声明一个空字典，用以存放提交的表单
    for hidden in hiddens: # 对于每一个隐藏的<input>标签
        form_data[hidden.get('name')] = hidden.get('value')  # 把name和value存到表单里
    nowTime = str(time.time()) # 获取当前时间戳
    replys = [
        u'6666666666666666666',
        u'I want to look what locked by louzhu.',
        u'There looking like exist something intersting.',
        u'learn something from this post.',
        u'Let me see what lz locked!'
    ]
    reply = replys[random.randint(0,4)]
    form_data['Char3'] = reply
    form_data['BTitle2'] = ''
    form_data['usesig'] = '1'
    form_data['emailnotify'] = 'on'
    form_data['postreplynotice'] = 'on' 
    form_data['replysubmit'] = ''
    form_data['handlekey'] = 'reply'
    # http://bbs.anjian.com/tools/ajax.aspx?topicid=536869&postid=0&postreplynotice=true&t=quickreply
    form_action = "http://" + domain + "/tools/ajax.aspx?topicid=" + str(tid) + "&postid=0&postreplynotice=true&t=quickreply" # 找到表单提交的地址，即处理页地址
    print form_action
    form_headers = {
        'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Cookie':Cookie,
        'Connection':'keep-alive'
    }
    print form_data
    form_data = urllib.urlencode(form_data)
    print form_data
    form_data2 = "BTitle2=&postlayer=-1&postid=0&handlekey=reply&usesig=1&emailnotify=on&postreplynotice=on&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&=&Char3=kankankankanhahaha&replysubmit="
    print form_data2
    request2 = urllib2.Request(form_action, form_data2, form_headers) # 往处理页发请求
    print request2
    response2 = urllib2.urlopen(request2)
    soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
    print soup2
    for i in range(1,6):
        time.sleep(1)
        print "因回复而延时",i,"秒"
    return
