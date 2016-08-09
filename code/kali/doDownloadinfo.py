# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "kali_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = '9f9q_746b_saltkey=p26Z7lIg; 9f9q_746b_lastvisit=1470226939; 9f9q_746b_lastact=1470230575%09misc.php%09patch; 9f9q_746b_sendmail=1; CNZZDATA1256836065=1931864543-1470228714-%7C1470228714; Hm_lvt_cb48ed518253dd6c5988e6eaa2af309e=1470230547; Hm_lpvt_cb48ed518253dd6c5988e6eaa2af309e=1470230580; Hm_lvt_2ba792dbf616f4e6810c53e2e602df55=1470230547; Hm_lpvt_2ba792dbf616f4e6810c53e2e602df55=1470230580; 9f9q_746b_seccode=6466.2e395a0a6bb59614ee; 9f9q_746b_dcaptchasig=h01af487909511a0f7031241c004c51b871b875108cc5f5435c5bf585811cf7b08d87d4025fa44a03fee481974f73763dc1031124a25d46f882bca825bbcd328e57; 9f9q_746b_ulastactivity=1470230568%7C0; 9f9q_746b_auth=0924MHVv1aJ5Fl1QJljxOXQygTU6DeyFef%2BLwxpf3GYPHUGgIV8td5awZzNrtUAdEF1Ud4hjPgfBpEhwbmjkCEHAJcM; 9f9q_746b_lastcheckfeed=432041%7C1470230568; 9f9q_746b_lip=221.2.164.41%2C1470230568; 9f9q_746b_security_cookiereport=675fYfGmgvYzJBLQpYjqaa08yiLElJ8Ey%2Ft30mFAbaqSkTXxHWL3; 9f9q_746b_nofocus_member=1; 9f9q_746b_connect_is_bind=0; 9f9q_746b_nofavfid=1; 9f9q_746b_onlineusernum=172; tjpctrl=1470232379969; 9f9q_746b_nofocus_forum=1'

for k in range(432976, 434300): #根据uid来获取用户资料页
    print '----------------------'
    try:
        url = 'http://www.kali.org.cn/home.php?mod=space&uid=' + str(k) + '&do=profile'
        downloadinfo(url,'www.kali.org.cn',Cookie,coll)
    except:
        f = open('baduid.txt','a')
        f.write(url + '  ----need cheek')
        f.write('\n')
        f.close()
        continue
