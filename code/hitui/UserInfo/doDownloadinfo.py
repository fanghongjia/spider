# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "hitui_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'EZjx_2702_saltkey=h12fv4zc; EZjx_2702_lastvisit=1470294099; EZjx_2702_lastact=1470297724%09misc.php%09patch; EZjx_2702_sendmail=1; pgv_pvi=4129653915; pgv_info=ssi=s5806912750; CNZZDATA3903802=cnzz_eid%3D2011534033-1470295847-%26ntime%3D1470295847; EZjx_2702_nofocus_forum=1; EZjx_2702_ulastactivity=1470297720%7C0; EZjx_2702_auth=fa75tnQTvzR%2FRahh8T3%2BQCRPJ6au5OiAf3M5AuEtrNDq58rcAuKygaYxm3gUGX2sbjSf5OOh85vUDHabHHALuQt2pRM; EZjx_2702_lastcheckfeed=100675%7C1470297720; EZjx_2702_checkfollow=1; EZjx_2702_lip=221.2.164.40%2C1470297720; EZjx_2702_connect_is_bind=0; EZjx_2702_checkpm=1; tjpctrl=1470299521732; EZjx_2702_nofavfid=1; pt_s_6f8e3865=vt=1470297724940&cad=; pt_6f8e3865=uid=kf5yj9gZYt6TIok17clb0A&nid=0&vid=VtY1OsFnDLEkYEDoFAdl/A&vn=1&pvn=3&sact=1470297724940&to_flag=0&pl=zzf1sYYpNnjxdEEBLz69sg*pt*1470297724940'

for k in range(1, 100675): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://bbs.hitui.com/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'bbs.hitui.com',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        f.close()
        continue
