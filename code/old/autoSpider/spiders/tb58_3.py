#coding:utf-8
import bs4
from bs4 import BeautifulSoup
import urllib2
import urllib
import MySQLdb
import re
import codecs
import sys
import math

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
'''
é¡µé¢ä¸è§„èŒƒçš„åœ°æ–¹ç”¨æ­£åˆ™åˆ†æž?
æ­£åˆ™æ¨¡æ¿è®¾ç½®
'''
compiled_time=re.compile(r'[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+')

board="干货分享"
'''
æ•°æ®åº?
'''
conn=MySQLdb.connect(host="172.26.253.87",user="root",passwd="YUgjBN",db="tb58",charset="utf8")
cursor = conn.cursor()
'''
å…¨å±€å˜é‡è®¾ç½®
'''
opener = urllib2.build_opener()
opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
#proxy_handler = urllib2.ProxyHandler({'http':'http://120.198.231.85:80'})
#opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)
for k in range(1,10):
	response = urllib2.urlopen('http://www.tb58.net/forum.php?mod=forumdisplay&fid=45&orderby=dateline&filter=author&orderby=dateline&page='+str(k))
	soup = BeautifulSoup(response,'lxml',from_encoding="utf-8")
	tagA = soup.findAll(name='a', attrs={'class':'s xst'})
	for title in tagA:				#æ¯ä¸ªå¸–å­ä¸€è½®å…¥åº?
		#print title.string
		args = []
		arg = []
		href = urllib.unquote(title['href'])
                try:
		    response2 = urllib2.urlopen(href)
                except:
                    continue
		soup2 = BeautifulSoup(response2,'lxml',from_encoding="utf-8")
		posts = soup2.findAll(attrs={'class':'pi'})		#postsä¸ºæœ¬é¡µæ‰€æœ‰å¸–å­?
		posts_contents = soup2.findAll(attrs={'class':'t_f'})
		try:
			author = posts[0].contents[1].contents[0].string		#ç¬¬iä¸ªå‘å¸–äºº
			time = compiled_time.search(str(posts[1])).group()	#å‘å¸–æ—¶é—´
		except:
			continue
			print "error1"
		print author,time,title.string
		arg = [title.string,author,time,href]
		args.append(arg)
				#print str(posts[1])		
				#print i
			#å¤„ç†æ¥¼ä¸»çš„å¸–å­?
			#louzhu_contents = posts_contents.pop(0)
			#print louzhu_contents
			#args[0].append('')
		i = 0
		for post_contents in posts_contents:
			if i == 1:
				break
			lines = post_contents.encode('utf-8')
			lines = re.sub('[?]','',lines)
			lines = re.sub('<span style=["]display:none["]>[^>]+>','',lines)
			lines = re.sub('<font class=["]jammer["]>[^>]+>','',lines)
			lines = re.sub('<(.*?)>','',lines)
			#re.sub('img','',lines)
			#lines = lines[90:]
			lines = lines.strip()
			args[i].append(lines.decode('utf-8').encode('utf-8'))
			print lines
			args[i].append(board)
			i+=1

		sql = "insert into contents(title,author,time,url,contents,board) values(%s,%s,%s,%s,%s,%s)"
		try:
			cursor.executemany(sql,args)
		except:
			print "error2"
		conn.commit()
			#print args
			#exit()
cursor.close()
conn.close()
print 'sucess!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
