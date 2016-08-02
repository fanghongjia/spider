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

Cookie = 'lSyb_2132_saltkey=Kg40257Y; lSyb_2132_lastvisit=1468581531; lSyb_2132_seccloud=1; lSyb_2132_ulastactivity=0a9cbknINVduHCTxXiLXiarSNbqKVKCpSv0oxb%2BwZSJRGDkrD8Zf; lSyb_2132_auth=0a9cbknINVduHCTxXifU0freO%2BuGB6n5SvsolL%2FkNHFZHzwrCJRct%2Ba4ruWRIkJczfxGwER1exgQOf5JwyxdGeq93g; lSyb_2132_lastcheckfeed=66273%7C1470112671; lSyb_2132_lip=221.2.164.35%2C1468469116; lSyb_2132_security_cookiereport=fd45dUKfdw%2FfBNzGdzg7Uk%2BcPCntE3c4ENvhMVFuZqoSVHL3mFsG; lSyb_2132_nofavfid=1; lSyb_2132_st_t=66273%7C1470112702%7Cfe08f61d998cdf8be00859517d586119; lSyb_2132_forum_lastvisit=D_3_1470112702; lSyb_2132_visitedfid=3; lSyb_2132_st_p=66273%7C1470112705%7C8ebe8171e767722e188ff470fd85e293; lSyb_2132_smile=1D1; lSyb_2132_seccode=99.4b36949da90dbde3dd; lSyb_2132_dcaptchasig=h013993349d8e1cd885e485c8a18014e5edd87a5fc16f78c00a2595f886a349ef93fb7f1120177dc272d30bad854d728035c8512f12fa5ad22ba51b3333c11f633c; lSyb_2132_viewid=uid_1; lSyb_2132_home_diymode=1; lSyb_2132_sid=q87E59; ad_play_index=45; pgv_pvi=7325971368; pgv_info=ssi=s2849227516; Hm_lvt_2c1faab5cf2d9e68bb23ccd8fa2dca4d=1468934176,1469104231,1470112658; Hm_lpvt_2c1faab5cf2d9e68bb23ccd8fa2dca4d=1470113504; lSyb_2132_lastact=1470114803%09forum.php%09ajax; lSyb_2132_connect_is_bind=0'

for k in range(1,66528): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://www.tianya88.com/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'www.tianya88.com',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        continue
