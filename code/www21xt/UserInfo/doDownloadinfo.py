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

Cookie = 'safedog-flow-item=; touclick-KeyboardBehavior=156C48927E6W1OEHPBH4K3FK8L07JHGQ; tjpctrl=1472196978619; vh2L_2132_saltkey=KtkaR0Hn; vh2L_2132_lastvisit=1472193383; vh2L_2132_sendmail=1; vh2L_2132_ulastactivity=c613yDeZjRk5YHlK2bC59HXljRKSOjnUAMAvGjSakFqJsRx9KcSS; vh2L_2132_auth=63d0NegYA5X19A9rJphQ%2F%2BV8zHgTI6EWWB3y0xFWMqIQMKF0S%2BfNb9Do6SYrc%2Fzk8juPSueYvAdlW99B32LVVF6k; vh2L_2132_lastcheckfeed=4675%7C1472196990; vh2L_2132_checkfollow=1; vh2L_2132_lip=222.175.198.22%2C1472196857; vh2L_2132_nofavfid=1; vh2L_2132_onlineusernum=46; vh2L_2132_study_nge_extstyle=auto; vh2L_2132_study_nge_extstyle_default=auto; vh2L_2132_sid=XDkMP5; vh2L_2132_checkpm=1; vh2L_2132_lastact=1472196994%09misc.php%09patch; vh2L_2132_connect_is_bind=0'

for k in xrange(3371, 4680): #根据uid来获取用户资料页 1-20333
    print '----------------------'
    for s in xrange(1, random.randint(4,10)):
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
