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

Cookie = 'EZjx_2702_saltkey=n2bJukP2; EZjx_2702_lastvisit=1470276246; EZjx_2702_auth=2ba1wODNeN6OEhmT6V8sK1zNRFu3S1Rq87R5UoSHICSZ5BNKT%2FLK550qmMVOhLn7R%2FiPoCnWvL9kqqVzFLefJXxQ1TY; EZjx_2702_nofavfid=1; EZjx_2702_atarget=1; EZjx_2702_ulastactivity=1470294223%7C0; tjpctrl=1470296025543; EZjx_2702_noticeTitle=1; EZjx_2702_nofocus_forum=1; EZjx_2702_sendmail=1; EZjx_2702_st_t=100675%7C1470294543%7Cd82b68453c5e9339b2e7eb146bb13f33; EZjx_2702_forum_lastvisit=D_38_1470279945D_56_1470294324D_110_1470294543; EZjx_2702_visitedfid=110D56D38; EZjx_2702_st_p=100675%7C1470294550%7Cb73ff742d1123b7662bfb6e6e01155cb; EZjx_2702_smile=1D1; EZjx_2702_viewid=uid_34629; EZjx_2702_home_diymode=1; EZjx_2702_checkpm=1; pt_6f8e3865=uid=BJ4/Ma5AIHKNIjQOV0uyfg&nid=0&vid=G0Gnd9klO91Gji7o378kvA&vn=2&pvn=22&sact=1470294640641&to_flag=0&pl=zzf1sYYpNnjxdEEBLz69sg*pt*1470294640641; pt_s_6f8e3865=vt=1470294640641&cad=; EZjx_2702_lastact=1470294655%09forum.php%09; EZjx_2702_connect_is_bind=0; pgv_pvi=2094726008; pgv_info=ssi=s2603229950; CNZZDATA3903802=cnzz_eid%3D99388485-1470279458-%26ntime%3D1470290446'

for k in range(1, 100675): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://bbs.hitui.com/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'bbs.hitui.com',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        continue
