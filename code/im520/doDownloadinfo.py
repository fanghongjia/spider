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

downloadinfo('http://bbs.im520.com/home.php?mod=space&uid=79&do=profile','bbs.im520.com','VJ8y_2132_saltkey=HGX3y3s1; VJ8y_2132_lastvisit=1469099336; VJ8y_2132_widthauto=-1; VJ8y_2132_nofavfid=1; VJ8y_2132_auth=4c35O%2F1t%2FJJl47mf9A1%2FXiR9r%2BJJu5WZhLugRl1VNtkydtUWgFkOBS6yoOZUFL6nFhPm%2BvMPhYufvEg%2FldfpqcWvusM; VJ8y_2132_lastcheckfeed=100124%7C1469795282; VJ8y_2132_ulastactivity=19be1NwPZur%2FcGUrEOJ7U4gqho6%2FIVCXoa6EyvgTi%2F9Ih8H0LlxM; VJ8y_2132_adclose_995=1; VJ8y_2132_visitedfid=15D157D73D189D19D23D133D8D41D36; VJ8y_2132_lastact=1469864228%09forum.php%09forumdisplay; VJ8y_2132_forum_lastvisit=D_53_1469193473D_171_1469193768D_77_1469194165D_163_1469195772D_103_1469195824D_4_1469195850D_165_1469195920D_174_1469195929D_89_1469195953D_49_1469195978D_13_1469195988D_146_1469196768D_144_1469255020D_36_1469255406D_41_1469255452D_8_1469255844D_133_1469446607D_23_1469447558D_19_1469450994D_189_1469451010D_73_1469451153D_157_1469795285D_15_1469864228; VJ8y_2132_sid=S6R53r; Hm_lvt_e70b0b6205f2208b96f42b05fcde8ef0=1469253091,1469446297,1469795260,1469864171; Hm_lpvt_e70b0b6205f2208b96f42b05fcde8ef0=1469864229; VJ8y_2132_smile=1D1',coll)
