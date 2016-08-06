# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

#网站域名
domain = "www.yjxsoft.com"

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "yjxsoft_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'jAx7_2132_saltkey=V737RR0r; jAx7_2132_lastvisit=1470465448; jAx7_2132_seccode=69.24a87006164cf2776b; jAx7_2132_ulastactivity=d60fEMd7UwN5ZeOJBKu3gTEHuj4bWIzVx7m6ehcIXiwI6DcIWgQn; jAx7_2132_auth=0d63kRLvXdViX0G5W4fLrbvRbDGDrxEpVOHlTPPzLDH%2BTr1L9%2BCt%2FXR6s5LpN1BZyjdU5oy2GBqmwdyBFsmY%2Bo1o4Q; jAx7_2132_security_cookiereport=d704Mq%2B%2BskJVJS5EMrKjfWhlxu%2F7uPXhnE7PFssxEFWnLfHbzsPb; jAx7_2132_nofavfid=1; jAx7_2132_onlineusernum=2427; tjpctrl=1470471144808; jAx7_2132_sendmail=1; jAx7_2132_noticeTitle=1; jAx7_2132_st_t=20333%7C1470469380%7C844f515d7e9fe2282c10cf1a4fb6387f; jAx7_2132_forum_lastvisit=D_44_1470469380; jAx7_2132_visitedfid=44; jAx7_2132_st_p=20333%7C1470469384%7C932ecb7e98f529d56f41076debc118d7; jAx7_2132_viewid=tid_2231; jAx7_2132_sid=Rw5iW5; pgv_pvi=1100759428; pgv_info=ssi=s2543286912; Hm_lvt_617c51f1f00a88e38a46ac3c234fded2=1470469047; Hm_lpvt_617c51f1f00a88e38a46ac3c234fded2=1470469383; jAx7_2132_smile=1D1; jAx7_2132_lastact=1470469473%09forum.php%09ajax; jAx7_2132_connect_is_bind=0'

for k in range(2985, 2986): #根据uid来获取用户资料页 1-20333
    print '----------------------'
    try:
        url = 'http://' + domain + '/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url, domain, Cookie, coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        f.close()
        continue
