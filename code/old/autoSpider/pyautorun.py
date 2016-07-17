#!/usr/bin/env python
#-- encoding:utf-8 --

"""
title:pyautorun
version:v0.2
author:倪远东
time:2016-03
lab:NISRC
email:niyuandong@wis-eye.com
"""

import sys
import time
import subprocess
from multiprocessing import Process
import thread
import os
import setting
import smtplib,email.utils
from email.mime.text import MIMEText
import traceback

# 主体类
class PyAuto:
    jobList = []
    tempfilePath=None
    mail_host=None
    mail_user=None
    mail_passwd=None
    mailto_List=[]
    mail_nick=None
    mail_switch=None

    # 构造函数
    def __init__(self):
        self.loadSetting()
        self.readIni()
        self.checkFolder()
        self.addJobs()

    # 载入setting.py中的相应配置信息
    def loadSetting(self):
        self.tempfilePath=setting.tempfilePath
        self.mail_host=setting.mail_host
        self.mail_user=setting.mail_user
        self.mail_passwd=setting.mail_passwd
        self.mailto_List=setting.mail_to_users
        self.mail_nick=setting.mail_sender_nickname
        self.mail_switch=setting.mailSwitch

    # 输出错误提示信息
    def printError(self,typeCode):
        print "ERROR:"
        if(typeCode == 0):
            print "jobs.ini文件不存在!"
        elif(typeCode == 1):
            print "jobs.ini文件为空!"
        sys.exit()

    # 读取jobs.ini文件中的作业列表
    def readIni(self):
        try:
            jobsFile = open("jobs.ini", 'a+')
        except:
            self.printError(0)
        lines = jobsFile.readlines()
        if(len(lines) == 0):
            self.printError(1)
        for line in lines:
            jobTemp = line.split(';', 3)
            timeStr = jobTemp[0].split(':')
            timeSec = int(timeStr[0]) * 24 * 60 * 60 + int(timeStr[1]) * \
                60 * 60 + int(timeStr[2]) * 60 + int(timeStr[3])
            jobTemp[0] = timeSec
            self.jobList.append(jobTemp)
        print self.jobList

    # 检查日志文件夹是否已经被创建，不存在则创建
    def checkFolder(self):
        if not os.path.exists(self.tempfilePath):
            os.mkdir(self.tempfilePath)

    # 获取当前的系统时间，以特定的格式返回
    def getCurrentTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

    # 实现执行单个作业任务的功能
    def runJob(self, interval, maxCount, runFlagStr, cmdLine):
        cmdLine=cmdLine.strip('\n')
        # 设置命令运行的计数值
        count=0
        try:
            if runFlagStr=="true":
                runFlag=True
            else:
                runFlag=False
        except:
            runFlag=True
        # 循环运行，间隔一定时间便执行作业
        while (count < maxCount):
            # 如果首次循环时从配置文件中读取的runFlag为False，则不会立即执行作业
            if runFlag:
                count+=1
                # 处理得到日志文件的文件名
                filename=cmdLine.replace(' ','_')
                filename=filename.replace('.','_')
                filename+=time.strftime("-%Y%m%d-%H_%M_%S",time.localtime(time.time()))
                filename+=".txt"
                filename=os.path.join(self.tempfilePath,filename)
                # 下面开始执行作业任务，并记录必要的信息
                startTime=self.getCurrentTime()
                cmdPro = subprocess.Popen(cmdLine, shell=True,stdout=subprocess.PIPE)
                # 等待子进程结束之后才执行下面的操作
                cmdPro.wait()
                endTime=self.getCurrentTime()
                print "TaskDone!    time: "+endTime+"    "+"pid: "+str(cmdPro.pid)+"    "+"conmand: "+cmdLine
                # 在日志文件中写入日志信息
                logFile=open(filename,'w+')
                logFile.write("运行命令:"+cmdLine+"\n")
                logFile.write("开始时间:"+startTime+"\n")
                logFile.write("结束时间:"+endTime+"\n")
                logFile.write("当前运行次数:"+str(count)+"\n")
                logFile.write("控制台输出内容:"+"\r\n")
                logFile.write(cmdPro.stdout.read())
                logFile.close()
                # 生成邮件标题
                if(count==maxCount):
                    mail_subject=cmdLine+"　　第"+str(count)+"次运行结束!（任务完结）"
                else:
                    mail_subject=cmdLine+"　　第"+str(count)+"次运行结束!"
                # 通过邮件开关判断发送邮件或仅输出信息
                if(self.mail_switch=='on'):
                    self.sendEmail(filename, mail_subject)
                else:
                    print mail_subject
            # 如果首次runFlag为假，则在此将他置为真
            else:
                runFlag=True
            #保证间隔运行的必要语句，及子线程睡眠指定的时间
            time.sleep(interval)

    # 拆分作业列表，利用多线程创建作业队列
    def addJobs(self):
        for job in self.jobList:
            #jobWork=Process(target=runJob, args=(job[1], job[0]))
            #jobWork.start()
            # 为便于主进程结束后对子作业进程进行回收，防止产生僵尸进程
            # 此处使用多线程来创建作业任务，而不是多进程
            thread.start_new_thread(self.runJob, (job[0],int(job[1]),job[2],job[3]))
        #保持主进程一直存活，直到人为杀死这个进程
        while True:
            pass


    # 邮件发送函数
    def sendEmail(self,content_file,mail_subject):
        content_type="plain"
        # 从日志文件中读取本次邮件内容
        f_content = open(content_file,'r+')
        content = f_content.read()
        f_content.close()
        # 设置邮件的发送信息
        msg = MIMEText(content,_subtype=content_type,_charset='utf8')    
        msg['From'] = email.utils.formataddr((self.mail_nick,self.mail_user)) 
        msg['To'] = email.utils.formataddr(('admin',self.mailto_List)) 
        msg['Subject'] = mail_subject
        msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
        try:
            # 尝试进行邮件发送
            # 连接邮件服务器
            server = smtplib.SMTP(self.mail_host) 
            # 登录邮箱
            server.login(self.mail_user,self.mail_passwd)
            # 发送邮件
            server.sendmail(self.mail_user,self.mailto_List,msg.as_string()) 
        except Exception,e:
            print mail_subject+' :SENDMAIL FAILED\n'
            print traceback.format_exc()
        else: 
            print mail_subject+' :SENDMAIL SUCCESS'
        finally: 
            server.close()




if __name__ == '__main__':
    PyAuto()
