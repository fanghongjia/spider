# coding:utf-8
from downloadinfo import downloadinfo
import pymongo
import time
import random

#网站域名
domain = "bbs.qqsky.net"

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "qqsky_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = '5j0w_2132_saltkey=el4lL7jg; 5j0w_2132_lastvisit=1470729023; 5j0w_2132_ulastactivity=e362kZzgq1tPaoPsANhtg1v1uG81p0m2glZe3av%2BfsanTw4c0Ltb; 5j0w_2132_auth=f951SL%2BJ1qjr6AbgE9GBIns3dsUN4Yq9ih1yJvYW4F576zQxyE7iFsySGexZhSCWpsBG%2Fc5fo1mN9K0hjz3DCUXpgn8; 5j0w_2132_lastcheckfeed=796396%7C1470810124; 5j0w_2132_security_cookiereport=4957Abql%2BPm6Kq00ss1fvUHrXk5CEXwsJ1%2B1xvAis3PUnv9x3IMy; 5j0w_2132_myrepeat_rr=R0; 5j0w_2132_nofavfid=1; 5j0w_2132_home_diymode=1; 5j0w_2132_visitedfid=6D12D83D3D20D11; 5j0w_2132_st_t=796396%7C1470814254%7C11b3f1cd84720c2ecd0d7016b6881495; 5j0w_2132_forum_lastvisit=D_11_1470732858D_20_1470810095D_3_1470814049D_12_1470814158D_6_1470814254; 5j0w_2132_viewid=tid_306722; 5j0w_2132_smile=3D1; 5j0w_2132_st_p=796396%7C1470814269%7Cc2ac4fbee8d9968fd3b8a0bd57028d40; safedog-flow-item=3F276922DF9F3B3D25F871ABCAFCEC8C; 5j0w_2132_lip=221.2.164.37%2C1470814273; 5j0w_2132_onlineusernum=4334; 5j0w_2132_sendmail=1; tjpctrl=1470817723557; 5j0w_2132_sid=QWXSt2; 5j0w_2132_lastact=1470815961%09misc.php%09patch; 5j0w_2132_connect_is_bind=0'

for k in range(3238, 796396): #根据uid来获取用户资料页 1-796396
    print '----------------------'
    try:
        url = 'http://' + domain + '/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url, domain, Cookie, coll)
        time.sleep(random.uniform(1, 7))
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        f.close()
        continue
