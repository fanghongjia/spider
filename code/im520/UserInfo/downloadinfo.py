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
reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')

#
# downloadinfo
# Description: 下载保存用户信息
# url: 用户信息的url
# domian: 网站的域名，例：bbs.2cto.com
# Cookie: 登录所获取的Cookie字符串
# coll： Mongodb数据库的操作手柄
#
def downloadinfo(url, domain, Cookie, coll):
    # 设置http报文的header信息
    opener = urllib2.build_opener()
    opener.addheaders = [
            ('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'),
            ('Cookie',Cookie),
            ('Connection','keep-alive')
        ]
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url) #打开这个资料页
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8") #解析这个资料页
    user = {} #声明一个空字典
    user['url'] = url
    top = soup.find(attrs = {'class':'bm_c u_profile'})
    if top == None:
        print "This uid is not exist!"
        f = open('baduid.txt','a')
        f.write(url + '  ----无此UID')
        f.write('\n')
        return
    counts = top.findAll(attrs = {'class':'pbm mbm bbda cl'})
    for count in counts:
        mbn = count.find(attrs = {'class':'mbn'})
        mbn_text = mbn.text
        if mbn_text == u'勋章':
            imgs = count.findAll(name = 'img')
            Medal = ''
            for img in imgs:
                Medal = Medal + img.get('alt') + '、'
            print u'勋章->' + Medal
            user['Medal'] = Medal
        elif mbn_text == u'管理以下版块':
            modules = count.findAll(name = 'a')
            AdminModule = ''
            for module in modules:
                AdminModule = AdminModule + module.string + '、'
            print u'管理以下版块','->',AdminModule
            user['AdminModule'] = AdminModule
        elif mbn_text == u'活跃概况':
            uls = count.findAll(name = 'ul')
            lis1 = uls[0].findAll(name = 'li')
            lis2 = uls[1].findAll(name = 'li')
            for li in lis1:
                ems = li.findAll(name = 'em')
                _as = li.findAll(name = 'a')
                i = 0
                for em in ems:
                    key = em.text.strip()
                    if key == u'管理组':
                        key = 'LevelAdministrator'
                        value = _as[i].string
                    elif key == u'用户组':
                        key = 'LevelUserGroup'
                        value = _as[i].string
                    elif key == u'扩展用户组':
                        key = 'ExLevelUserGroup'
                        value = li.find(name = 'font').text
                    print key, '->', value
                    user[key] = value
                    i = i + 1
            for li in lis2:
                ems = li.findAll(name = 'em')
                i = 0
                for em in ems:
                    key = em.text
                    value = li.text
                    value = value.replace(key, '')
                    if key == u'在线时间':
                        key = 'TimeOnLine'
                    elif key == u'注册时间':
                        key = 'RegistrationData'
                    elif key == u'卖家好评度':
                        key = 'TheSellerRating'
                    elif key == u'最后访问':
                        key = 'DateLastAccessed'
                    elif key == u'注册IP':
                        key = 'IPRegistered'
                    elif key == u'上次访问IP':
                        key = 'IPLastVisited'
                    elif key == u'上次活动时间':
                        key = 'DateLastActivity'
                    elif key == u'上次发表时间':
                        key = 'DateLastPosted'
                    elif key == u'所在时区':
                        key = 'TimeZone'
                    print key, '->', value
                    user[key] = value
        else:
            mbn = count.find(attrs = {'class':'mbn'})
            UserName = mbn.text
            UID = mbn.find(attrs = {'class':'xw0'}).text
            if mbn.find(name = 'img') == None:
                UserName = UserName.replace(UID, '')[2:-1] #切片去掉换行符
            else:
                UserName = UserName.replace(UID, '')[2:-3] #切片去掉换行符
            uid_compile= re.compile(r'[0-9]+')
            UID = uid_compile.search(str(UID)).group()
            print 'UserName->', UserName
            print 'UID->', UID 
            user['UserName'] = UserName
            user['UID'] = UID
            uls = count.findAll(name = 'ul')
            for ul in uls:
                lis = ul.findAll(name = 'li')
                ems = ul.findAll(name = 'em')
                i = 0
                for li in lis:
                    if ems[i].text == u'统计信息':
                        _as = li.findAll(name = 'a')
                        for a in _as:
                            value_compile= re.compile(r'[0-9]+')
                            value = value_compile.search(str(a.string)).group()
                            key = a.string
                            key = key.replace(value, '')
                            key = key.strip()
                            if key == u'好友数':
                                key = 'NumFriends'
                            elif key == u'回帖数':
                                key = 'NumReply'
                            elif key == u'主题数':
                                key = 'NumPost'
                            print key, '->', value
                    else:
                        key = ems[i].text.strip()
                        if key == 'QQ':
                            value = li.find(name = 'a').get('href')
                            value_compile= re.compile(r'[0-9][0-9]+')
                            value = value_compile.search(str(value)).group()
                        else:        
                            value = li.text
                            value = value.replace(key, '')
                        i = i + 1
                        if key == u'空间访问量':
                            key = 'NumSpaceVisited'
                        elif key == u'邮箱状态':
                            key = 'EmailStatus'
                        elif key == u'视频认证':
                            key = 'VideoAuthenticationStatus'
                        elif key == u'自定义头衔':
                            key = 'Title'
                        elif key == u'个人签名':
                            key = 'Signature'
                        elif key == u'性别':
                            key = 'Sex'
                        elif key == u'生日':
                            key = 'Birthday'
                        elif key == u'学历':
                            key = 'Education'
                        elif key == u'阿里旺旺':
                            key = 'Alitalk'
                        elif key == u'个人主页':
                            key = 'HomePage'
                        print key, '->', value
                    user[key] = value
    cl = top.find(attrs = {'class':'cl', 'id':'psts'})
    pfl_lis = cl.find(attrs = {'class':'pf_l'}).findAll(name = 'li')
    ems = cl.find(attrs = {'class':'pf_l'}).findAll(name = 'em')
    i = 0
    for pfl_li in pfl_lis:
        key = ems[i].text
        value = pfl_li.text
        value = value.replace(key, '')
        if key == u'已用空间':
            key = 'UsedSpace'
        elif key == u'买家好评度':
            key = 'TheBuyersRating'
        elif key == u'卖家好评度':
            key = 'TheSellerRating'
        elif key == u'积分':
            key = 'MemberPoint'
        elif key == u'银行':
            key = 'BankCardInformation'
        elif key == u'信用':
            key = 'Credit'
        elif key == u'Ｉ币':
            key = 'I-Money'
        elif key == u'Ｍ币':
            key = 'M-Money'
        elif key == u'推广':
            key = 'NumExpanded'
        elif key == u'娱乐':
            key = 'Entertainment'
        elif key == u'捐赠':
            key = 'Donations'
        elif key == u'贡献':
            key = 'Contribution'
        print key, '->', value
        user[key] = value
        i = i + 1
    coll.insert(user)

