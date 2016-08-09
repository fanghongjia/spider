# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "eyuyan_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

# 网站域名
domain = "bbs.eyuyan.com"

Cookie = 'e5da7_ipstate=1470716588; e5da7_winduser=AwMAU1YCa10DCgBaBgZVDFYFUFUMUFFRUwBQAQdSAwBcClAGBVUGag; e5da7_ck_info=%2F%09; e5da7_readlog=%2C312250%2C312400%2C312380%2C312392%2C312397%2C312396%2C312395%2C320749%2C371737%2C11111%2C; e5da7_cknum=BQACU1YFVwkEDGxrBwBRDwoFBVUCVQMGVgwCDgFWBFUFWFIMAg1XVFIFU1w; e5da7_threadlog=%2C124%2C148%2C116%2C119%2C149%2C159%2C128%2C160%2C; e5da7_ol_offset=4365; e5da7_c_stamp=1470729222; e5da7_lastpos=index; e5da7_lastvisit=5780%091470729222%09%2Findex.php'

for k in range(4815, 4816): #根据uid来获取用户资料页1-775109
    print '-----------------------------'
    try:
        url = 'http://' + domain + '/u.php?a=info&uid=' + str(k)
        downloadinfo(url, domain, Cookie, coll)
    except:
        print 'something need cheek!'
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek') # 可能是有什么东西没解析出来或者有特殊情况
        f.write('\n')
        f.close()
        continue
