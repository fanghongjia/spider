# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "tianya88_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'lSyb_2132_saltkey=Kg40257Y; lSyb_2132_lastvisit=1468581531; lSyb_2132_nofavfid=1; lSyb_2132_forum_lastvisit=D_3_1470112702; lSyb_2132_visitedfid=3; lSyb_2132_smile=1D1; lSyb_2132_seccloud=1; lSyb_2132_home_diymode=1; lSyb_2132_seccode=42.70c6fcbcc9944fd4fe; lSyb_2132_dcaptchasig=h01f5a18b615e09abb8175fc6cb6584063a1075e82e1408c7de0e8ea1a1bc53544170922cbc5a833d773814aa0e52bdeafbcdfed08b9c2d2f54b77782162b22c005; lSyb_2132_ulastactivity=36991GukR5wwn6uNQnlq%2F7EM%2BzEIIyHrTEKW4mYzHzTm5lkRuSe0; lSyb_2132_auth=36991GukR5wwn6uNQnk5p%2BBZ%2FTEIdHG8EEqbtjtnTmfu4VUWvHK%2Bpib3QAC1cqy9VPPmVuoXa6uURn6ErguB51VKzA; lSyb_2132_lastcheckfeed=66273%7C1470185408; lSyb_2132_security_cookiereport=a2b7Bor%2BJ7ldNZ7K2qU2vaU0X%2FwWsT9t3acCWcpBj%2BGDP2RzRf99; tjpctrl=1470187213713; lSyb_2132_sid=bssn3E; ad_play_index=74; pgv_pvi=7325971368; pgv_info=ssi=s5679073738; Hm_lvt_2c1faab5cf2d9e68bb23ccd8fa2dca4d=1468934176,1469104231,1470112658,1470185086; Hm_lpvt_2c1faab5cf2d9e68bb23ccd8fa2dca4d=1470185430; lSyb_2132_connect_is_bind=0; lSyb_2132_lastact=1470185430%09like.php%09'

for k in range(1, 65814): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://www.tianya88.com/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'www.tianya88.com',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        continue
