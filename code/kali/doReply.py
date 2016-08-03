# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import time
import sys
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
    html=response.read()
    print html
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8") #解析这个帖子
    form_div = soup.find(attrs={'class':'pl bm bmw'}) # 找到包含回复表单的div
    form = form_div.find(name='form') # 找到表单
    hiddens = form_div.findAll(attrs={'type':'hidden'}) # 找到表单内的隐藏域
    form_data = {} # 声明一个空字典，用以存放提交的表单
    for hidden in hiddens: # 对于每一个隐藏的<input>标签
        form_data[hidden.get('name')] = hidden.get('value')  # 把name和value存到表单里
    # 通过数据包分析得表单里除了隐藏域还有message和posttime两项
    nowTime = str(time.time()) # 获取当前时间戳
    reply = u'I really like this card!' + nowTime
    form_data['message'] = reply
    form_data['posttime'] = nowTime
    print form_data
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
    for i in range(1,11):
        time.sleep(1)
        print "因回复而延时",i,"秒"
    return

if __name__=="__main__":
    doReply('http://www.kali.org.cn/thread-18366-1-1.html','www.kali.org.cn','9f9q_746b_saltkey=HCqR667Z; 9f9q_746b_lastvisit=1468919730; 9f9q_746b_atarget=1; 9f9q_746b_auth=bdc5b0qwSFW5Y504Vs%2FVO%2BDCMPw2ZXTW3nT8gbksVAcmQnUvAuUyXYoNGBgyd%2FVZGfIxJ5VNbqfn%2Bj4h0RGCdnedZX0; 9f9q_746b_lastcheckfeed=432041%7C1468923512; 9f9q_746b_nofavfid=1; 9f9q_746b_security_cookiereport=6f7aqDlikJBOuFB%2Fi86ue6%2FJgb2YIIT%2BohTkph34RNsv6EtOAV7Z; 9f9q_746b_visitedfid=68D21D5D9D62; tjpctrl=1470211000994; 9f9q_746b_home_diymode=1; 9f9q_746b_st_t=432041%7C1470209826%7Cb8cf5b625f32511fe7ee640a902bfc6f; 9f9q_746b_forum_lastvisit=D_5_1470111867D_21_1470206804D_68_1470209826; 9f9q_746b_ulastactivity=1470209826%7C0; 9f9q_746b_st_p=432041%7C1470209829%7Ccf46ac4cf8a9fddac30ede551731ffc9; 9f9q_746b_viewid=tid_18366; 9f9q_746b_seccode=3855.8b58288ac6880f7f7c; 9f9q_746b_dcaptchasig=h01f664f7dcb860cfee2f574af9c6cd8fa0e7d2ac2c92b8423ba0de548829b06c5f81963880d576b7bcfe5f0dcfcc902233d7f0ecfc0d73da5d95bfa1368aad2b1d; CNZZDATA1256836065=1065794573-1468920054-%7C1470207029; Hm_lvt_cb48ed518253dd6c5988e6eaa2af309e=1468923335,1470106547,1470206798; Hm_lpvt_cb48ed518253dd6c5988e6eaa2af309e=1470210104; Hm_lvt_2ba792dbf616f4e6810c53e2e602df55=1468923335,1470106566,1470206798; Hm_lpvt_2ba792dbf616f4e6810c53e2e602df55=1470210104; 9f9q_746b_lastact=1470210102%09connect.php%09check; 9f9q_746b_connect_is_bind=0; 9f9q_746b_nofocus_forum=1')
