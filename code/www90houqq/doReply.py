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
    formhash = ""
    for hidden in hiddens: # 对于每一个隐藏的<input>标签
        if hidden.get('name') == 'formhash':
            formhash = hidden.get('value')
    # 通过数据包分析得表单里除了隐藏域还有message
    nowTime = str(time.time()) # 获取当前时间戳
    replys = [
       '%bf%b4%bf%b4%bf%b4%bf%b4%bf%b4%bf%b4',
       '%bb%d8%b8%b4%b2%e9%bf%b4%d2%fe%b2%d8%c4%da%c8%dd',
       '%bb%d8%b8%b4%b2%e9%bf%b4%d2%f7%b3%aa%c4%da%c8%dd',
       '%bf%b4%bf%b4%ca%c7%ca%b2%c3%b4%ba%c3%b6%ab%b6%ab',
       '%ba%c3%ba%c3%bf%b4%cc%fb%a3%ac%cc%ec%cc%ec%cf%f2%c9%cf'
    ]
    reply = replys[random.randint(0,4)]
    form_action = "http://" + domain + "/" + form.get('action') + "&inajax=1" # 找到表单提交的地址，即处理页地址
    form_headers = {
        'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Cookie':Cookie,
        'Connection':'keep-alive'
    }
    form_data = "message=" + reply + "&formhash=" + formhash + "&usesig=&subject=++"
    request2 = urllib2.Request(form_action, form_data, form_headers) # 往处理页发请求
    response2 = urllib2.urlopen(request2)
    soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
    print soup2
    for i in range(1,10):
        time.sleep(1)
        print "因回复而延时",i,"秒"
    return
