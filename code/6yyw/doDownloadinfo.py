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

Cookie = 'TmYt_2132_saltkey=uFs3s6fJ; TmYt_2132_lastvisit=1470272701; TmYt_2132_seccode=24.a14b65b3cef6fdf016; TmYt_2132_ulastactivity=0b1fa5Tap2iNwfgBd802jBU9o4Z3MJ7LvWo6PpjDCML03R7JgWrY; TmYt_2132_auth=789ekx90rTOdl7JMa06LPI%2FyEX93j2NAu5PhyK6G%2FyHayj4kRX%2BsetQaMfl9GEDPtpaf9NkM%2FvLlDRPcOjUxhrTRSg; TmYt_2132_nofavfid=1; tjpctrl=1470278225658; TmYt_2132_atarget=1; TmYt_2132_connect_not_sync_feed=1; TmYt_2132_connect_not_sync_t=1; TmYt_2132_adclose_=1; TmYt_2132_lip=221.2.164.39%2C1470278078; TmYt_2132_home_diymode=1; TmYt_2132_sendmail=1; TmYt_2132_noticeTitle=1; TmYt_2132_st_t=40486%7C1470278151%7Ca156c6e70dd6e3d140018ad27facd747; TmYt_2132_forum_lastvisit=D_75_1470276422D_39_1470276496D_68_1470278151; TmYt_2132_visitedfid=68D36D39D70D75; TmYt_2132_st_p=40486%7C1470278162%7C862d290b409e107cac7544f5625ac548; TmYt_2132_viewid=tid_63284; TmYt_2132_sid=jslg8k; pgv_pvi=9132249503; pgv_info=ssi=s5518194700; a3536_pages=26; a3536_times=1; amvid=c25a4f23965baf79186a3aa7abe81646; TmYt_2132_smile=1D1; TmYt_2132_lastact=1470278169%09forum.php%09ajax; TmYt_2132_connect_is_bind=0'

for k in range(40486, 40487): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://www.6yyw.com/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'www.6yyw.com',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        continue
