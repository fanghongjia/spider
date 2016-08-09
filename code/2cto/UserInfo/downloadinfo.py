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
    print "URL->",url
    user['URL'] = url
    
    boxA = soup.find(attrs = {'class':'boxA'})
    if boxA == None:
        print "This uid is not exist!"
        f = open('baduid.txt','a')
        f.write(url + '  ----无此UID')
        f.write('\n')
        f.close()
        return
    UserName = boxA.find(attrs = {'class':'f14 b'}).string
    print 'UserName->', UserName
    user['UserName'] = UserName
    Signature = boxA.findAll(attrs = {'class':'mb5'})[2].text
    print 'Signature->', Signature
    user['Signature'] = Signature
    Medals = boxA.findAll(name = 'div')[1].findAll(name = 'img')
    Medal = ''
    for medal in Medals:
        Medal = Medal + medal.get('title') + '、'
    print 'Medal->', Medal
    user['Medal'] = Medal
    uls = boxA.findAll(name = 'ul')
    lis1 = uls[1].findAll(name = 'li')
    for li in lis1:
        key = li.find(name = 'p').text
        if key == u'关注':
            key = 'AttentionNum'
        elif key == u'粉丝':
            key = 'Fans'
        elif key == u'访客':
            key = 'NumSpaceVisited'
        value = li.find(name = 'span').text
        print key, '->', value
        user[key] = value
    lis2 = uls[2].findAll(name = 'li')
    for li in lis2:
        spans = li.findAll(name = 'span')
        key = spans[0].text
        if key == u'认证：':
            key = 'Qualification'
            imgs = li.findAll(name = 'img')
            value = ''
            for img in imgs:
                value = value + img.get('title') + '、'
        else:
            if key == u'等级：':
                key = 'LevelUserGroup'
            elif key == u'身份：':
                key = 'levelAdminstrator'
            elif key == u'总积分：':
                key = 'MemberPoints'
            value = spans[1].text
        print key, '->', value
        user[key] = value
        
    boxB = soup.find(attrs = {'class':'boxB'})
    ths = boxB.findAll(name = 'th')
    tds = boxB.findAll(name = 'td')
    i = 0
    for th in ths:
        th = th.text
        if th == u'会员头衔':
            th = 'VIPTitle'
        elif th == u'系统头衔':
            th = 'SysTitle'
        elif th == u'在线时间':
            th = 'TimeOnLine'
        elif th == u'性别':
            th = 'Sex'
        elif th == u'生日':
            th = 'Birthday'
        elif th == u'现居住地':
            th = 'CurrentResidence'
        elif th == u'家乡':
            th = 'Hometown'
        elif th == u'支付宝账号':
            th = 'Apliy'
        elif th == u'个人主页':
            th = 'HomePage'
        elif th == u'自我介绍':
            th = 'SelfIntroduce'
        elif th == u'注册时间':
            th = 'RegistrationData'
        elif th == u'最后登录':
            th = 'DataLastAccessed'
        elif th == u'精华帖子':
            th = 'EssencePosts'
        elif th == u'帖子':
            th = 'NumReply'
        elif th == u'平均日发帖':
            th = 'PostsPerDay'
        elif th == u'帖子签名':
            th = 'PostsSignature'
        elif th == u'工作经历':
            th = 'WorkExperience'
        elif th == u'教育经历':
            th = 'EducationExperience'
        td = tds[i].text
        print th, '->', td
        user[th] = td
        i = i + 1
    coll.insert(user)

