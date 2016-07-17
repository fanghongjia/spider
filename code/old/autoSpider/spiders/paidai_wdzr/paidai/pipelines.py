# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

'''
目标数据库
'''
db_des_host = '172.26.253.87';
db_des_port = 3306;
db_des_username = 'root';
db_des_password = 'YUgjBN';
db_des_name = 'paidai';
db_des_tablename ='contents';

class PaidaiPipeline(object):
    def process_item(self, item, spider):
        insertSql = "insert into " + db_des_tablename + "(title,author,time,url,contents,board) values(%s,%s,%s,%s,%s,%s);" 
        sqlArg=[item['title'].encode("utf-8") ,item['author'].encode("utf-8") ,item['time'].encode("utf-8") ,item['url'],item['contents'].encode("utf-8"),item['board'].encode("utf-8")]
        desConn = self.getDesMysqlConn()
        desCur=desConn.cursor()
        desCur.execute(insertSql,sqlArg)
        desCur.close()
        desConn.commit()
        desConn.close()
        return item

    def getDesMysqlConn(self):
        return MySQLdb.connect(host= db_des_host,user=db_des_username,passwd= db_des_password,db=db_des_name,port=db_des_port,charset="utf8")

