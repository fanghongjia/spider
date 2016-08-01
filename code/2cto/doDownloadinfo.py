# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "2cto_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = '02b4a_cloudClientUid=53525456; home__username=kongtianyi2; 02b4a_winduser=ClAGBwBTOgwCCgsCDFMKVgAFC1QBDwYGBQQOXAQCCgBaUgQCBV8GPg; modelguidehide=1; 02b4a_ol_offset=291; 02b4a_threadlog=%2C66%2C18%2C20%2C12%2C72%2C49%2C43%2C90%2C33%2C25%2C; 02b4a_readlog=%2C325302%2C269953%2C358419%2C152898%2C332123%2C337860%2C337872%2C318488%2C375355%2C375514%2C; 02b4a_ci=index%091470031517%09%09; 02b4a_lastpos=other; 02b4a_lastvisit=20%091470031519%09%2Fy.php%3Factionsync%26nowtime1470031930063%26verify6abe2b5e; Hm_lvt_1898984a3d796e86ad73ad1f4bc9f240=1468557776,1468586892,1469447797,1470016040; Hm_lpvt_1898984a3d796e86ad73ad1f4bc9f240=1470032010; Hm_lvt_7a3d919664d39f5547bd796a73d9b0a8=1470031991; Hm_lpvt_7a3d919664d39f5547bd796a73d9b0a8=1470032010'

for k in range(209927,209928): #根据uid来获取用户资料页
    print '-----------------------------'
    try:
        url = 'http://bbs.2cto.com/u.php?a=info&uid=' + str(k)
        downloadinfo(url,'bbs.2cto.com',Cookie,coll)
    except:
        print 'something need cheek!'
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek') # 可能是有什么东西没解析出来或者有特殊情况
        f.write('\n')
        continue
