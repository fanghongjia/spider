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
def doReply(url, domain, Cookie):
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
    form_div = soup.find(attrs={'class':'pl bm bmw'}) # 找到包含回复表单的div
    if form_div == None:
        return
    form = form_div.find(name='form') # 找到表单
    if form == None:
        return
    hiddens = form_div.findAll(attrs={'type':'hidden'}) # 找到表单内的隐藏域
    form_data = {} # 声明一个空字典，用以存放提交的表单
    for hidden in hiddens: # 对于每一个隐藏的<input>标签
        form_data[hidden.get('name')] = hidden.get('value')  # 把name和value存到表单里
    # 通过数据包分析得表单里除了隐藏域还有message
    nowTime = str(time.time()) # 获取当前时间戳
    replys = [
        u'6666666666666666666',
        u'I want to look what locked by louzhu.',
        u'There looking like exist something intersting.',
        u'learn something from this post.',
        u'Let me see what lz locked!'
    ]
    reply = replys[random.randint(0,4)]
    form_data['message'] = reply
    form_data['posttime'] = nowTime
    form_action = "http://" + domain + "/" + form.get('action') + "&inajax=1" # 找到表单提交的地址，即处理页地址
    form_headers = {
        'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Cookie':Cookie,
        'Connection':'keep-alive'
    }
    form_data = urllib.urlencode(form_data)
    request2 = urllib2.Request(form_action, form_data, form_headers) # 往处理页发请求
    response2 = urllib2.urlopen(request2)
    soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
    print soup2
    for i in range(1,181):
        time.sleep(1)
        print "因回复而延时",i,"秒" # 每小时限回复20贴
    return
