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
# coll： Mongodb数据库collection的操作手柄
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
    top = soup.find(attrs = {'class':'bm_c u_profile'})
    if top == None:
        print "This uid is not exist!"
        f = open('baduid.txt','a')
        f.write(url + '  ----无此UID')
        f.write('\n')
        f.close()
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
            print u'Medal->' + Medal
            user['Medal'] = Medal
        elif mbn_text == u'用户认证':
            imgs = count.findAll(name = 'img')
            Qualification = ''
            for img in imgs:
                Qualification = Qualification + img.get('alt') + '、'
            print u'Qualification->' + Qualification
            user['Qualification'] = Qualification
        elif mbn_text == u'管理以下版块':
            modules = count.findAll(name = 'a')
            AdminModule = ''
            for module in modules:
                AdminModule = AdminModule + module.string + '、'
            print u'AdminModule','->',AdminModule
            user['AdminModule'] = AdminModule
        elif mbn_text == u'名人堂状态':
            ps = count.findAll(name = 'p')
            for p in ps:
                value = p.find(name = 'font').text
                key = p.text
                if key == u'该用户是名人堂成员':
                    continue
                key = key.replace(value, '')
                if key == u'名人堂组别: ':
                    key = 'LevelHallOfFame'
                elif key == u'用户介绍: ':
                    key = 'UserIntroduce'
                print key, '->', value
                user[key] = value
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
                    elif key == u'最后访问':
                        key = 'DateLastAccessed'
                    elif key == u'注册 IP':
                        key = 'IPRegistered'
                    elif key == u'上次访问 IP':
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
                            try:
                                value = value_compile.search(str(a.string)).group()
                            except:
                                value = '0'
                            key = a.string
                            key = key.replace(value, '')
                            key = key.strip()
                            if key == u'好友数':
                                key = 'NumFriends'
                            elif key == u'记录数':
                                key = 'NumRecord'
                            elif key == u'日志数':
                                key = 'NumJournal'
                            elif key == u'相册数':
                                key = 'NumAlbum'
                            elif key == u'回帖数':
                                key = 'NumReply'
                            elif key == u'主题数':
                                key = 'NumPost'
                            elif key == u'分享数':
                                key = 'NumShare'
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
                        elif key == u'最新记录':
                            key = 'LastRecord'
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
                        elif key == u'交友目的':
                            key = 'MakeFriendsAim'
                        elif key == u'阿里旺旺':
                            key = 'Alitalk'
                        elif key == u'出生地':
                            key = 'Hometown'
                        elif key == u'居住地':
                            key = 'CurrentResidence'
                        elif key == u'个人主页':
                            key = 'HomePage'
                        print key, '->', value
                    user[key] = value
    c = top.find(attrs = {'class':'bm bbda cl'})
    if c != None:
        ps = c.findAll(name = 'p')
        if ps[0].text != u'该会员从未签到':
            user['AllSignInTime'] = ps[0].find(name = 'b').text
            print 'AllSignInTime->', user['AllSignInTime']
            user['SerialSignInTime'] = ps[1].find(name = 'b').text
            print 'SerialSignInTime->', user['SerialSignInTime']
            user['ThisMonthSignInTime'] = ps[2].find(name = 'b').text
            print 'ThisMonthSignInTime->', user['ThisMonthSignInTime']
            user['LastSignInTime'] = ps[3].find(name = 'font').text
            print 'LastSignInTime->', user['LastSignInTime']
            user['AllReward'] = ps[4].text
            print 'AllReward->', user['AllReward']
            if ps[5].find(name = 'b') != None:
                user['SignInLevel'] = ps[5].find(name = 'b').text
                print 'SignInLevel->', user['SignInLevel'] 
    cl = top.find(attrs = {'class':'cl', 'id':'psts'})
    pfl_lis = cl.find(attrs = {'class':'pf_l'}).findAll(name = 'li')
    ems = cl.find(attrs = {'class':'pf_l'}).findAll(name = 'em')
    Money = {} # 各式各样的交易币存成一类
    i = 0
    for pfl_li in pfl_lis:
        key = ems[i].text
        value = pfl_li.text
        value = value.replace(key, '')
        if key == u'已用空间':
            key = 'UsedSpace'
        elif key == u'积分':
            key = 'MemberPoint'
        elif key == u'威望':
            key = 'Prestige'
        elif key == u'学币':
            key = 'Money'
            Money['Learn-Money'] = value
        elif key == u'贡献':
            key = 'Contribution'
        elif key == u'银元':
            key = 'Money'
            Money['Sliver-Money'] = value
        elif key == u'下载点':
            key = 'DownloadPoint'
        elif key == u'荣誉':
            key = 'Honours'
        elif key == u'信誉':
            key = 'HonestyLevel'
        elif key == u'好评度':
            key = 'PositiveComment'
        elif key == u'活跃':
            key = 'Active'
        print key, '->', value
        if key != 'Money':
            user[key] = value
        i = i + 1
    user['Money'] = Money
    coll.insert(user)


