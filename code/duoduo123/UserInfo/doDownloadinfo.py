# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

#网站域名
domain = "bbs.duoduo123.com"

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "duoduo123_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'jAx7_2132_saltkey=SH9S3BiD; jAx7_2132_lastvisit=1470466695; pgv_pvi=3567020556; Hm_lvt_617c51f1f00a88e38a46ac3c234fded2=1470470302; jAx7_2132_ulastactivity=b568xC%2FBD9VbJa%2BaV6GHm1oxzubRBvCLPnHsC94XFb3oBbDkS4il; jAx7_2132_auth=4beaw%2BDjuCfmv54SysdJQkAWMXZlr%2FB0bBkHfj%2BFop9tysLbkuae6J5dU4YEZZHu35p1LBXpKkiyVkQRnsFZRtAnyQ; jAx7_2132_lastcheckfeed=20333%7C1470470310; jAx7_2132_connect_is_bind=0; jAx7_2132_nofavfid=1; jAx7_2132_lip=221.2.164.37%2C1470620185; pgv_info=ssi=s7870907270; Hm_lpvt_617c51f1f00a88e38a46ac3c234fded2=1470620469; jAx7_2132_sid=jD1n4d; jAx7_2132_creditnotice=0D0D2D0D0D0D0D0D0D20333; jAx7_2132_creditbase=0D0D720D0D0D0D0D0D0; jAx7_2132_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; jAx7_2132_lastact=1470620484%09home.php%09spacecp; jAx7_2132_security_cookiereport=7225r10y6zOjxgDVTIq32ZIxBn8hu9OSYAlI8WGi6zZKdCE0SEx2; jAx7_2132_onlineusernum=1111; jAx7_2132_sendmail=1; jAx7_2132_checkpm=1; jAx7_2132_noticeTitle=1'

for k in range(13167, 236593): #根据uid来获取用户资料页 1-236593
    print '----------------------'
    try:
        url = 'http://' + domain + '/home.php?mod=space&uid=' + str(k)
        downloadinfo(url, domain, Cookie, coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        f.close()
        continue
