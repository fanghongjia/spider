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
# domian: 网站的域名，例：www.tianya88.com
# Cookie: 登录所获取的Cookie字符串
# coll： Mongodb数据库的操作手柄
#
def downloadinfo(url, domain, Cookie, coll):
    # 设置http报文的header信息
    opener = urllib2.build_opener()
    opener.addheaders = [
            ('Connection', 'keep-alive'),
            ('Cookie', Cookie),
            ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36')           
        ]
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url) #打开这个资料页
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8") #解析这个资料页
    user = {} #声明一个空字典
    user['url'] = url
    print 'URL->', url
    top = soup.find(attrs = {'class':'uc_main'})
    if top == None:
        print "This uid is not exist!"
        f = open('baduid.txt','a')
        f.write(url + '  ----无此UID')
        f.write('\n')
        f.close()
        return

    count1 = top.find(attrs = {'class':'itemtitle cl'})
    UserName = count1.find(name = 'h1').text
    print 'UserName ->',UserName
    user['UserName'] = UserName
    UID = count1.find(name = 'li').text
    UID = re.findall(r'[0-9]+', UID, re.I)[0]
    print 'UID ->',UID
    user['UID'] = UID
    
    count2 = top.find(attrs = {'id':'baseprofile'})
    ths = count2.findAll(name = 'th')
    tds = count2.findAll(name = 'td')
    i = 0
    for th in ths:
        th = th.text
        td = tds[i].text
        if th == u'性别: ':
            th = 'Sex'
            td = td.replace('\t', '')
            td = td.replace('\r\n', '')
        elif th == u'生日: ':
            th = 'Birthday'
        elif th == u'QQ: ':
            th = 'QQ'
        print th, '->', td
        user[th] = td
        i += 1
    
    h3s = top.findAll(name = 'h3')
    Level = h3s[0].text
    Level = Level.replace('\r\n', '')
    Level = Level.replace(' ', '')
    Level = Level.replace('\n', '')
    Level = Level[6:]
    print 'LevelUserGroup ->', Level
    user['LevelUserGroup'] = Level
    MemberPoints = h3s[1].text
    MemberPoints = re.findall(r'[0-9]+', MemberPoints, re.I)[0]
    print 'MemberPoints ->', MemberPoints

    count3 = top.findAll(attrs = {'class':'cl'})[1]
    lis = count3.findAll(name = 'li')
    labels = count3.findAll(name = 'label')
    i = 0
    for li in lis:
        value = li.text
        key = labels[i].text
        value = value.replace(key, '')
        if key == u'昵称:':
            key = 'ForkName'
        elif key == u'阅读权限:':
            key = 'ReadPermission'
        elif key == u'发帖量:':
            key = 'NumReply'
        elif key == u'精华帖数:':
            key = 'EssencePosts'
        elif key == u'在线时间:':
            key = 'TimeOnline'
        elif key == u'注册日期:':
            key = 'RegistrationData'
        elif key == u'最后访问(登录):':
            key = 'DataLastAccessed'
        elif key == u'最后活动:':
            key = 'DataLastActivity'
        print key, '->', value
        user[key] = value
        i += 1
    
    count4 = top.findAll(name = 'p')
    p = count4[-1].text
    nums = re.findall(r'[0-9]+', p, re.I)
    Money = {}
    Money['flower-Money'] = nums[0]
    Money['copper-Money'] = nums[1]
    Money['sliver-Money'] = nums[2]
    Money['gold-Money'] = nums[3]
    print 'Money ->', Money
    user['Money'] = Money 
    coll.insert(user)


