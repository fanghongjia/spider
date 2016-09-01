# coding:utf-8
from downloadinfo import downloadinfo
import pymongo
import random
import time

#网站域名
domain = "bbs.qqsky.net"

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "qqsky_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = '5j0w_2132_saltkey=uoTuUuEU; 5j0w_2132_lastvisit=1470812897; 5j0w_2132_sid=FHcgCV; 5j0w_2132_lastact=1470816577%09misc.php%09patch; 5j0w_2132_sendmail=1; 5j0w_2132_onlineusernum=4367; 5j0w_2132_ulastactivity=49a1iHUN5FfUlK1LNILr7qT4q79ntfZhC6dEfh%2Boi0jex%2B%2BsmAAV; 5j0w_2132_auth=c443Y6hs6m%2Fhtxy3mutfyYSvjwfGXThGUzuyNkT0xetf2cKZvZgkf%2FN%2BR2espi0BgQA8KewJpxeIMrk9YC6a0YXk0qc; 5j0w_2132_lastcheckfeed=796396%7C1470816574; 5j0w_2132_checkfollow=1; 5j0w_2132_lip=221.2.164.39%2C1470815923; 5j0w_2132_security_cookiereport=6759xlOU4khueaFNoWM0270cbNKPxJhSY%2FyCaQVoh0ES1pbuECKQ; 5j0w_2132_connect_is_bind=0; 5j0w_2132_nofavfid=1; 5j0w_2132_myrepeat_rr=R0; 5j0w_2132_checkpm=1; tjpctrl=1470818381103'

for k in xrange(796396, 561422, -1): #根据uid来获取用户资料页 1-796396
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
    for t in range(1, int(random.uniform(1, 3))):
        time.sleep(1)
        print "sleep", t, "s"
