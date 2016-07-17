#-*-coding:utf8-*-
import pymongo

connection = pymongo.MongoClient(host='192.168.204.129', port=12345)
tdb = connection['class31']
post_info = tdb.students

zhangtong = {'name': u'张通', 'age':'21', 'skill':{'1':u'坑爹','2':'chishi'}}
xujie = {'name': u'许洁', 'age':'20', 'grade':'670'}
# post_info.insert(zhangtong)
post_info.insert(zhangtong)
# post_info.remove({'name': u'张通'})
print 'database action go over!'
