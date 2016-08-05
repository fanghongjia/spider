# coding:utf-8
from selenium import webdriver

driver = webdriver.PhantomJS() # 使用浏览器访问
driver.get('http://www.kali.org.cn/') # 打开主页

# 模拟登陆
username = 'kongtianyi'
password = 'k1234567890'
elem_user = driver.find_element_by_id('ls_username')
elem_pwd = driver.find_element_by_id('ls_password') 
elem_user.send_keys(username)  
elem_pwd.send_keys(password)  
elem_sub = driver.find_element_by_xpath('//*[@id="lsform"]/div/div[1]/table/tbody/tr[2]/td[3]/button')
elem_sub.click()

page = dirver.get('http://www.kali.org.cn/thread-17602-1-1.html') 
print page.page_source #这就是返回的页面内容了，与urllib2.urlopen().read()的效果是类似的，但比urllib2强在能抓取到动态渲染后的内容。
driver.quit()
