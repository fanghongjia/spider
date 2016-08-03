# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "blackbap_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'B96o_2132_saltkey=ZuegE46S; B96o_2132_lastvisit=1470101431; B96o_2132_seccode=121.86bc7d56af73c2e987; B96o_2132_ulastactivity=5812%2BgKvLpALssJc%2F4oygtXC9FfPzVzEr1K%2BS0Fg6pC5ekfeAIom; B96o_2132_auth=779dXl4hxTNuKW52cry9Fpnb%2BrcQYeUbVHimfwmUG55WmqGMZJiwL7%2F9%2BWNPApHjvMLquGj%2FOLeGA%2Fqwsv9i7aYijA; B96o_2132_lastcheckfeed=11297%7C1470192983; B96o_2132_lip=202.102.144.8%2C1470144275; B96o_2132_st_p=11297%7C1470193015%7C9564b2074cda4d18f2667a94241f9819; B96o_2132_viewid=tid_8134; B96o_2132_nofavfid=1; B96o_2132_onlineusernum=338; B96o_2132_visitedfid=21D10D11D29D18; B96o_2132_st_t=11297%7C1470193134%7C9558bf09ae6e0822557429aa374107b4; B96o_2132_forum_lastvisit=D_18_1470105356D_29_1470105808D_11_1470192986D_10_1470193102D_21_1470193134; B96o_2132_smile=4D1; B96o_2132_sid=G6xvwg; B96o_2132_checkpm=1; B96o_2132_sendmail=1; B96o_2132_lastact=1470193227%09misc.php%09patch'

for k in range(1, 11299): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://bbs.blackbap.org/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'bbs.blackbap.org',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        continue
