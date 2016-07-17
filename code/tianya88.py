# coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import pymongo
import re
import codecs
import sys
import math

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
----------------------相关全局变量---------------------
'''
# 需要爬取的板块连接（注意该链接下的帖子是按照发帖时间进行排序的，且去掉最后的数字）
spiderUrl = "http://www.tianya88.com/forum.php?mod=forumdisplay&fid=22&orderby=dateline&filter=author&orderby=dateline&page="
# 入库存储的板块名称
board = "幽默笑话"
# 该板块内需要爬取的起始页号
page_start = 1
# 该板块内需要爬取的终止页号
page_end = 9
# 代理服务器
proxy_server = 'http://120.198.231.85:80'
# 数据库信息
mongodbHost = "172.29.152.230"
mongodbPort = 27017
db_name = "spider"
coll_name = "tianya88"

'''
---------------------------------------------------------
'''

# 用于匹配日期的正则表达式
compiled_time = re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')
# 数据库的连接信息
connection = pymongo.MongoClient(host=mongodbHost, port=mongodbPort)
connection.admin.authenticate("nslab","nslab")
db = connection[db_name]
coll = db[coll_name]
# 设置http报文的header信息
opener = urllib2.build_opener()
opener.addheaders = [
    ('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
    ('Cookie','lSyb_2132_saltkey=ySj79Jq7; lSyb_2132_lastvisit=1468319031; lSyb_2132_seccloud=1; lSyb_2132_st_p=0%7C1468457559%7Ca2ba1e0da393ac3f6643d05ec69b8eaf; lSyb_2132_viewid=tid_5802; lSyb_2132_visitedfid=49D50D91D72D71D73D42D41D19D18; lSyb_2132_forum_lastvisit=D_4_1468322631D_6_1468322942D_46_1468326401D_45_1468327855D_5_1468391371D_8_1468392298D_44_1468393085D_9_1468396142D_10_1468397323D_38_1468398281D_28_1468398951D_29_1468399177D_30_1468399401D_31_1468399832D_32_1468400135D_33_1468400551D_34_1468402384D_39_1468402671D_86_1468403356D_87_1468407092D_88_1468410899D_89_1468412315D_90_1468412926D_98_1468414784D_14_1468414791D_15_1468415040D_16_1468415539D_17_1468415818D_18_1468416177D_19_1468416387D_41_1468416420D_42_1468416594D_43_1468456023D_73_1468456034D_71_1468456386D_72_1468456837D_91_1468457056D_50_1468457521D_49_1468457624; lSyb_2132_seccode=116.36778faff82ac0f577; lSyb_2132_dcaptchasig=h0156c17dbf4aad63b53ad9fb05e73527f268af568f4894ffd41303fb4639e39439560af636ed9b7e64f94670a99596be6d0be36b6c7d945eb79ac769936fa28864; lSyb_2132_ulastactivity=714dNlpFNF%2BPlBn5DF1IU4Lzm%2BPV%2FY7sKCA48Y7zKaOgXYG4Y4vr; lSyb_2132_auth=714dNlpFNF%2BPlBn5DFgWA4X2ybTSq4XvLXU%2BpY6nePGgX4C9atzoLbhL5GCFVy9jDpfMRu8yuzwfpalEtLlTqKtA%2BQ; lSyb_2132_lastcheckfeed=66273%7C1468457821; lSyb_2132_lip=221.2.164.3%2C1468330858; lSyb_2132_security_cookiereport=ee4cgdY7mTEHxYprjJDKzTKldp7OrSPUfbl3Dtp8MNtZ5Kn49xnm; lSyb_2132_nofavfid=1; lSyb_2132_onlineusernum=122; lSyb_2132_sendmail=1; tjpctrl=1468459627352; lSyb_2132_st_t=66273%7C1468457851%7Ceeffc866ac9c7f8816cb63d87d7f6907; lSyb_2132_sid=QCCM38; ad_play_index=383; pgv_pvi=6040145672; pgv_info=ssi=s4026210906; Hm_lvt_2c1faab5cf2d9e68bb23ccd8fa2dca4d=1468248740,1468248873,1468391207,1468409789; Hm_lpvt_2c1faab5cf2d9e68bb23ccd8fa2dca4d=1468457857; lSyb_2132_noticeTitle=1; lSyb_2132_lastact=1468457857%09misc.php%09patch; lSyb_2132_connect_is_bind=0'),
    ('Connection','keep-alive')
    ]
# 以下两行用于设置代理，一般情况下无需使用
# proxy_handler = urllib2.ProxyHandler({'http':proxy_server})
# opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
for k in range(page_start, page_end):
    response = urllib2.urlopen(spiderUrl + str(k))
    soup = BeautifulSoup(response, 'lxml', from_encoding="utf-8")
    tagA = soup.findAll(name='a', attrs={'class': 's xst'})
    # 依次解析每一个帖子标题
    for title in tagA:
        # 从标题中提取帖子的链接，访问该链接从中解析出帖子更多信息
        href = urllib.unquote(title['href'])
        # href = "http://bbs.125.la/"+href
        try: 
            response2 = urllib2.urlopen(href)
            soup2 = BeautifulSoup(response2, 'lxml', from_encoding="utf-8")
        except:
            print "bad url!"
            continue
        p_page_content = soup2.find(attrs={'class':'pg'})
        if(p_page_content != None):
            p_page_url_init = p_page_content.contents[1].get('href')[0:-1]
            p_page_end = p_page_content.find(name='span').string
            compiled_page = re.compile(r'[0-9]+')
            p_page_end = int(compiled_page.search(str(p_page_end)).group())
            # print p_page_end,"!!!!!!"
        else:
            p_page_end = 1
            print "-------------------------------------"
        newItem = {} # 初始化一个新帖子字典
        flag = True # 识别是不是楼主的flag
        for l in range(1, p_page_end+1):
            if(p_page_content != None):
                p_page_url = p_page_url_init + str(l)
            else:
                p_page_url = href
            # print p_page_url
            try:
                response3 = urllib2.urlopen(p_page_url)
                soup3 = BeautifulSoup(response3, 'lxml', from_encoding="utf-8")
            except:
                print "bad url!"
                continue
            posts = soup3.findAll(attrs={'class': 'pi'})
            posts_contents = soup3.findAll(attrs={'class': 't_f'})
            # 以下循环将正文部分处理成一整个字符串形式
            i = 1

            for post_contents in posts_contents:
                try:
                    author = posts[2*(i-1)].contents[1].contents[0].string
                    time = compiled_time.search(str(posts[2*(i-1)+1])).group()
                    floor = '';
                    floor = floor + str(posts[2*(i-1)+1].contents[1].contents[1].find(name = 'em'))
                    floor = floor[4:-5]
                    if(floor == ''):
                        floor = posts[2*(i-1)+1].contents[1].contents[1].string[2:]
                except:
                    print "ERROR:获取作者、时间、楼层信息出错！"
                    continue
                lines = post_contents.encode('utf-8')
                lines = re.sub('[?]', '', lines)
                lines = re.sub('<span style=["]display:none["]>[^>]+>', '', lines)
                lines = re.sub('<font class=["]jammer["]>[^>]+>', '', lines)
                lines = re.sub('<(.*?)>', '', lines)
                # re.sub('img','',lines)
                # lines = lines[90:]
                lines = lines.strip()
                # args[i].append(lines.decode('utf-8').encode('utf-8'))
                print lines
                # 整理数据
                if(i == 1 and flag == True):
                    first_floor = {
                        'author':author,
                        'title':title.string,
                        'floor':1,
                        'content':lines,
                        'href':href,
                        'board':board,
                        'time':time
                    }
                    print "爬到",time,title.string,"了"
                    newItem['1'] = first_floor
                    flag = False
                else:
                    other_floor = {
                        'content':lines,
                        'time':time,
                        'floor':floor,
                        'author':author
                    }
                    newItem[floor] = other_floor
                i += 1
        try:
            coll.insert(newItem)
        except:
            print "ERROR:数据库存储错误！"
print "板块 " + board + " 爬取结束！"
