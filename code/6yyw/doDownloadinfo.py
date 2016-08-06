# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "6yyw_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'TmYt_2132_saltkey=uFs3s6fJ; TmYt_2132_lastvisit=1470272701; TmYt_2132_nofavfid=1; TmYt_2132_atarget=1; TmYt_2132_st_t=0%7C1470446534%7Ce1ea26f05fddda0a57f2e64e59f051b0; TmYt_2132_forum_lastvisit=D_39_1470276496D_68_1470278210D_75_1470446534; TmYt_2132_visitedfid=36D75D70D68D39; TmYt_2132_ulastactivity=95cbKpLXDymRaY5IW1AChu1iEnA8KgPhrBWnnszr52aRuD2o5sKC; TmYt_2132_auth=1ac6ijJGY10%2BXsXgc2Jtv%2FIQXagsAy5vIVqzxv5AArZAEk4nk0jilU7ff5qZqAhNS7IAzHoSR4ktfiTZvk1WsAdxWA; TmYt_2132_lastcheckfeed=40486%7C1470446543; TmYt_2132_lip=222.175.198.19%2C1470446543; TmYt_2132_st_p=40486%7C1470446544%7Cf243ad8c8fc1ec4cb762f0c2475eafe1; TmYt_2132_viewid=tid_53981; TmYt_2132_sid=M6aaAb; pgv_pvi=9132249503; pgv_info=ssi=s3704636706; a3536_pages=4; a3536_times=2; amvid=a612d0bc1be6748b6eb6c4922e40ef67; TmYt_2132_smile=1D1; tjpctrl=1470448655641; TmYt_2132_lastact=1470446628%09forum.php%09ajax; TmYt_2132_connect_is_bind=0'

for k in range(40486, 40487): #根据uid来获取用户资料页
    print '----------------------'
    #try:
    url = 'http://www.6yyw.com/home.php?mod=space&uid=' + str(k) + '&do=profile'
    downloadinfo(url,'www.6yyw.com',Cookie,coll)
    #except:
    #    f = open('baduid.txt','a')
    #    f.write(url + '  ----need cheek')
    #    f.write('\n')
    #    continue
