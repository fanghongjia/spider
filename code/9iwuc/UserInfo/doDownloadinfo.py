# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "9iwuc_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'kUgw_2132_saltkey=Y2B6f7f7; kUgw_2132_lastvisit=1469095487; _uab_collina=146909886790173929168546; kUgw_2132_nofavfid=1; kUgw_2132_home_readfeed=1469099176; kUgw_2132_visitedfid=2D40D39D45; kUgw_2132_smile=1D1; kUgw_2132_pc_size_c=0; _umdata=BA335E4DD2FD504F96A2511DD5D63351664B4C74DC9F52D0356162481D878590D38322107110972C700668F9A382A3D6FD4E024474DA7742C89A7C1207D0654A877A329830844C53E17171FE4CB309C842B5BA42E9BF5B4FF1D69141C3C4FD27; kUgw_2132_ulastactivity=f47aYYIk7lgh0kBE1JDU%2FAvKEXID9HDo2bygB9SuQQGd%2B7OnzcOj; kUgw_2132_auth=5815zDAka8ayiaX08NBHRoYJ%2BS0nIZ837Q9ZdUTfEJ7y%2F98gRJhsrkFBuEgtixbhXsPs6dCB2sYUpuPggFK%2FUgsl; kUgw_2132_lastcheckfeed=2671%7C1470191168; kUgw_2132_lip=222.175.198.19%2C1470191168; kUgw_2132_onlineusernum=18; tjpctrl=1470192742262; kUgw_2132_sendmail=1; kUgw_2132_home_diymode=1; kUgw_2132_sid=afiDvY; kUgw_2132_lastact=1470191321%09misc.php%09patch; kUgw_2132_connect_is_bind=0'

for k in range(1, 2946): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://www.9iwuc.com/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'www.9iwuc.com',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        continue
