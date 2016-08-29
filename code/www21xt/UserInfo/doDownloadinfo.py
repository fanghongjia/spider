# coding:utf-8
from downloadinfo import downloadinfo
import pymongo
import random
import time

#网站域名
domain = "www.21xt.net"

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "www21xt_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'vh2L_2132_saltkey=l80w80Ct; vh2L_2132_lastvisit=1472215866; vh2L_2132_sid=VXFdVf; vh2L_2132_lastact=1472219493%09misc.php%09patch; safedog-flow-item=; vh2L_2132_sendmail=1; vh2L_2132_ulastactivity=e144E6dg0GbQ813kS2oTILcuyvP6J7R%2BQvzkYXWx0AOWjhgqnTnY; vh2L_2132_auth=cfc6wh0P4e0T2Yc0PpagcjldYAWYETbuVIjvIQ%2BmYRaRnNLkZXndiBY5emCPm0KshxFag%2Fs8NjaeQaQl5DgAmZEv; vh2L_2132_lastcheckfeed=4675%7C1472219491; vh2L_2132_checkfollow=1; vh2L_2132_lip=222.175.198.15%2C1472215499; vh2L_2132_connect_is_bind=0; vh2L_2132_nofavfid=1; vh2L_2132_onlineusernum=51; vh2L_2132_study_nge_extstyle=auto; vh2L_2132_study_nge_extstyle_default=auto; vh2L_2132_checkpm=1; tjpctrl=1472221260906'

for k in xrange(3826, 4680): #根据uid来获取用户资料页 1-20333
    print '----------------------'
    for s in xrange(1, random.randint(6,10)):
        print 'sleep'
        time.sleep(1)
    try:
        url = 'http://' + domain + '/space-uid-' + str(k) + '.html'
        downloadinfo(url, domain, Cookie, coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        f.close()
        continue
