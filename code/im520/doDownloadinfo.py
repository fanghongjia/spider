# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "im520_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'VJ8y_2132_saltkey=doK6JY0w; VJ8y_2132_lastvisit=1469936095; VJ8y_2132_sid=xf7VQQ; VJ8y_2132_lastact=1469976481%09home.php%09spacecp; Hm_lvt_e70b0b6205f2208b96f42b05fcde8ef0=1469939697; Hm_lpvt_e70b0b6205f2208b96f42b05fcde8ef0=1469976483; VJ8y_2132_adclose_995=1; VJ8y_2132_ulastactivity=3d91rP1%2FaTk9q4FGTOQNDuRH%2FZotdUl9mfLNpM2eogWIE4xsdxws; VJ8y_2132_auth=2bc8c57rPEO1pXmip8KkF%2BcIPOQ4DkAUwZQvg83XUfmNER8nOrjzdYfbQMNUGa6Jxo478X2zTN7dnDOFLobTQ9aI7h0; VJ8y_2132_lastcheckfeed=100124%7C1469939888; VJ8y_2132_nofavfid=1; VJ8y_2132_forum_lastvisit=D_49_1469940147; VJ8y_2132_visitedfid=49; VJ8y_2132_smile=1D1; VJ8y_2132_onlineusernum=1514; VJ8y_2132_sendmail=1; VJ8y_2132_viewid=uid_100127; VJ8y_2132_home_diymode=1; tjpctrl=1469978239524; VJ8y_2132_checkpm=1'

for k in range(54543,100128): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://bbs.im520.com/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'bbs.im520.com',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        continue
