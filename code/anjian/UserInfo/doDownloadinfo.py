# coding:utf-8
from downloadinfo import downloadinfo
import pymongo

domain = 'bbs.anjian.com'

# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "anjian_info"

# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]

Cookie = 'pgv_pvid=8490825450; dntVC=QyG3wKFGWZBLQW8ifAC5xNteYmIvemPAt0yR00npppA=; pgv_pvi=9974319104; ASP.NET_SessionId=fg3qdanvx4r2bkvrixlvcwaa; __qc_wId=519; editormode_e=-1; lastposttitle=d41d8cd98f00b204e9800998ecf8427e; lastpostmessage=044c4166484acba78aa0155aadc1a99d; lastolupdate=906174319; lastposttime=2016-08-11 15:41:49; forumpageid=2; visitedforums=233,207,244,17,234,250,221,219,245,240; dnt=userid=4060473&password=5dIPmdcddfIGzNTTBinEwTZdBnDxp2V5Qo07Z8MeQ3qiAllJwJPaAA%3d%3d&tpp=0&ppp=0&pmsound=0&invisible=0&referer=showtopic.aspx%3ftopicid%3d482893%26page%3d1%26auctionpage%3d1%26forumpage%3d1&sigstatus=1&expires=43200&userinfotips=&visitedforums=17%2c244%2c221%2c250%2c234%2c245%2c56%2c219%2c233%2c66%2c240&oldtopic=D482893D443800D115802D106865D536869D106864D119443D339118D343260D543440D565244D591352D569461; dntusertips=userinfotips=%e7%a7%af%e5%88%86%3a11%2c%e7%94%a8%e6%88%b7%e7%bb%84%3a%3cfont+color%3d%22FF6500%22%3e%e6%8c%89%e9%94%ae%e7%b2%be%e7%81%b5%e4%bc%9a%e5%91%98%3c%2ffont%3e%2c%e9%b2%9c%e8%8a%b1%3a+0%e6%9c%b5%2c%e9%93%9c%e5%b8%81%3a+39%e4%b8%aa%2c%e9%93%b6%e5%b8%81%3a+0%e4%b8%aa%2c%e9%87%91%e5%b8%81%3a+0%e4%b8%aa; lastactivity=onlinetime=908785775&oltime=908785775; allowchangewidth=; AJSTAT_ok_pages=47; AJSTAT_ok_times=4; Hm_lvt_5d96b144d9b7632ed0ce359527dcc65d=1470820593,1470821337,1470821363,1470877578; Hm_lpvt_5d96b144d9b7632ed0ce359527dcc65d=1470903961'

for k in range(2653357, 2653358): #根据uid来获取用户资料页
    print '----------------------'
    #try:
    # http://bbs.anjian.com/userinfo.aspx?userid=1822798
    url = 'http://' + domain + '/userinfo.aspx?userid=' + str(k)
    downloadinfo(url, domain, Cookie, coll)
    #except:
    #    f = open('baduid.txt','a')
    #    f.write(url + '  ----need cheek')
    #    f.write('\n')
    #    f.close()
    #    continue
