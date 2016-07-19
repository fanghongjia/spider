# coding:utf-8
# 验证码识别，此程序只能识别数据验证码 
import Image 
import ImageEnhance 
import ImageFilter 
import sys 
import pytesseract
# from pytesser import *
# 二值化 
threshold = 140
table = [] 
for i in range(256): 
 if i < threshold: 
  table.append(0) 
 else: 
  table.append(1) 

def getverify1(name):   
 #打开图片 
 im = Image.open(name) 
 #转化到灰度图 
 imgry = im.convert('L') 
 #保存图像 
 imgry.save('g'+name) 
 #二值化，采用阈值分割法，threshold为分割点 
 out = imgry.point(table,'1') 
 out.save('b'+name) 
 #识别 
 text = pytesseract.image_to_string(out) 
 #识别对吗 
 text = text.strip() 
 text = text.upper();  
 #out.save(text+'.jpg') 
 print text 
 return text 
getverify1('idcode.jpg') #注意这里的图片要和此文件在同一个目录，要不就传绝对路径也行 
