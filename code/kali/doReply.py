# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import time
import sys
import random
import json
import api # 打码接口
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
    print soup
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
        u'揭开楼主的秘密',
        u'May I can get something useful!'
    ]
    reply = replys[random.randint(0,4)]
    form_data['message'] = reply
    form_data['posttime'] = nowTime

    seccodeverify_str = api.main(
        'kongtianyi',
        'k1234567890',
        'http://www.kali.org.cn/plugin.php?id=cloudcaptcha:get&rand=DN1h277ar0',
        "http://bbb4.hyslt.com/api.php?mod=php&act=upload",
        '',
        '',
        '0',
        '')
    seccodeverify_dict = json.loads(seccodeverify_str)
    seccodeverify = seccodeverify_dict['data']['val']
    form_data['seccodeverify'] = seccodeverify

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
    for i in range(1,6):
        time.sleep(1)
        print "因回复而延时",i,"秒"
    return

if __name__=="__main__":
    doReply('http://www.kali.org.cn/thread-18014-1-1.html', 'www.kali.org.cn', 'CNZZDATA1253188052=1852896376-1470213199-http%253A%252F%252Fwww.kali.org.cn%252F%7C1470213199; 9f9q_746b_saltkey=b8IJPiif; 9f9q_746b_lastvisit=1470377080; 9f9q_746b_atarget=1; 9f9q_746b_auth=e2c1ugeEexlrz6YCsmmS19I4pRZfdTUliFJIbV24D1lPv8oFStLvJPDwt4JYGSuASaZeIiZ%2B7g%2FgKufACi5ZCEqrQ%2Bo; 9f9q_746b_lastcheckfeed=432041%7C1470465712; 9f9q_746b_security_cookiereport=86bcBzfXCgrakzeOwqTK2bOXH%2BXp8F7GefuWhul7zETSlFIl2HVo; 9f9q_746b_nofavfid=1; 9f9q_746b_ulastactivity=1470474924%7C0; tjpctrl=1470476726193; 9f9q_746b_st_t=432041%7C1470474929%7C91cca0dcdc52100659448e2d10db9744; 9f9q_746b_forum_lastvisit=D_8_1470380685D_21_1470467305D_68_1470474929; 9f9q_746b_visitedfid=68D21D8; 9f9q_746b_st_p=432041%7C1470474932%7C33c2bfe634263fe05dc560ff379acb8a; 9f9q_746b_viewid=tid_16717; 9f9q_746b_seccode=3899.382b6dca30b3ac3cd9; 9f9q_746b_dcaptchasig=h0156d0bce25abae9dd37cf71b44a5f1aad2ee5400544a199f2eb08028b2524b6fb9a3cc067ad468ff318aa8490d37ea95fadba067bfb4efcdb08e8443228ce12b5; Hm_lvt_cb48ed518253dd6c5988e6eaa2af309e=1470206798,1470378278,1470459422,1470474926; Hm_lpvt_cb48ed518253dd6c5988e6eaa2af309e=1470475476; CNZZDATA1256836065=1065794573-1468920054-%7C1470475475; Hm_lvt_2ba792dbf616f4e6810c53e2e602df55=1470206798,1470378278,1470459422,1470474926; Hm_lpvt_2ba792dbf616f4e6810c53e2e602df55=1470475476; 9f9q_746b_lastact=1470475474%09connect.php%09check; 9f9q_746b_connect_is_bind=0')
