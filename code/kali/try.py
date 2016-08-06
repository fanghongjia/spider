# coding:utf-8
from selenium import webdriver

driver = webdriver.PhantomJS('/home/kongwei/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs') # 使用浏览器访问
driver.get('http://www.tianya88.com/') # 打开主页

# 模拟登陆
username = 'kongtianyi'
password = 'k1234567890'
elem_user = driver.find_element_by_id('ls_username')
elem_pwd = driver.find_element_by_id('ls_password')
elem_ckt = driver.find_element_by_id('ls_cookietime')
elem_user.send_keys(username)  
elem_pwd.send_keys(password)
elem_ckt.send_keys('1')  
elem_sub = driver.find_element_by_xpath('//*[@id="lsform"]/div/div[1]/table/tbody/tr[2]/td[3]/button')
elem_sub.click()

elem_check = driver.find_element_by_xpath('//*[@id="seccodeverify_cSAVxwy5w"]')
elem_img = driver.find_element_by_xpath('//*[@id="seccode_jscSAVxwy5w"]/img')

img_src = elem_img.get_attribute("src")
print img_src


#driver.get('http://www.tianya88.com/forum.php?mod=viewthread&tid=101945') 
#print driver.page_source #这就是返回的页面内容了，与urllib2.urlopen().read()的效果是类似的，但比urllib2强在能抓取到动态渲染后的内容。
driver.quit()
plugin.php?id=cloudcaptcha:get&rand=ZKcSFSfkPu&modid=forum::viewthread&refresh=0
plugin.php?id=cloudcaptcha:get&rand=U87ulknYUj&modid=undefined&refresh=1
plugin.php?id=cloudcaptcha:get&rand=Tc66dDM6Rj&modid=undefined&refresh=1
plugin.php?id=cloudcaptcha:get&rand=W1j1SsfSlJ&modid=forum::viewthread&refresh=0
plugin.php?id=cloudcaptcha:get&rand=cw6f7i9bw7&modid=forum::viewthread&refresh=0
