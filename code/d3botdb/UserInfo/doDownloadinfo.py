# coding:utf-8
from downloadinfo import downloadinfo
import pymongo
import random
import time

#网站域名
domain = "bbs.d3botdb.com"

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "d3botdb_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = ''

for k in xrange(5660, 7000): #根据uid来获取用户资料页 1-25067
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