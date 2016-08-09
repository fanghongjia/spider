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

Cookie = '02b4a_lastpos=other; 02b4a_ol_offset=388; home__username=kongtianyi2; 02b4a_cloudClientUid=48575549; 02b4a_winduser=CA8EVgIAaAsKBgZUAw1UUA8EBAEHVwFSAA9eAAZTBwlXAVdQAFoGbw; 02b4a_lastvisit=16%091470273942%09%2Fu.php; Hm_lvt_1898984a3d796e86ad73ad1f4bc9f240=1470274363; Hm_lpvt_1898984a3d796e86ad73ad1f4bc9f240=1470274363'

for k in range(654668,654669): #根据uid来获取用户资料页
    print '-----------------------------'
    # try:
    url = 'http://bbs.2cto.com/u.php?a=info&uid=' + str(k)
    downloadinfo(url,'bbs.2cto.com',Cookie,coll)
    # except:
    #     print 'something need cheek!'
    #     f = open('baduid.txt','a')
    #     f.write(url + '  ----need cheek') # 可能是有什么东西没解析出来或者有特殊情况
    #     f.write('\n')
    #     f.close()
    #     continue
