#coding=utf-8
from appium import webdriver
from time import sleep

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1.1'
desired_caps['deviceName'] = 'Test26'
#UC56
desired_caps['appPackage'] = 'com.uc56.ucexpressbao'
desired_caps['appActivity'] = '.activitys.SplashActivity'

# desired_caps['unicodeKeyboard'] = True  # 使用unicodeKeyboard的编码方式来发送字符串
# desired_caps['resetKeyboard'] = True  # 将键盘给隐藏起来
second = 3;
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
sleep(3);
# #手机号码
# driver.find_element_by_id("com.uc56.ucexpressbao:id/phone_num").send_keys('15079442008')
# sleep(1);
# #网点编号
# driver.find_element_by_id("com.uc56.ucexpressbao:id/web_id").send_keys('02017')
# sleep(1);
# #员工编号
# driver.find_element_by_id("com.uc56.ucexpressbao:id/employee_id").send_keys('0201717')
# sleep(1);
# #员工密码
# driver.find_element_by_id("com.uc56.ucexpressbao:id/password").send_keys('111111111')
# sleep(1);
# driver.find_element_by_id("com.uc56.ucexpressbao:id/save_password").click()
# sleep(1);
# driver.find_element_by_id("com.uc56.ucexpressbao:id/save_password").click()
# sleep(1);
# driver.find_element_by_id("com.uc56.ucexpressbao:id/login_button").click()
# sleep(1);

#忘记密码com.uc56.ucexpressbao:id/forget_password
# driver.find_element_by_id("com.uc56.ucexpressbao:id/forget_password").click() #是否重置密码
# sleep(1);
# #忘记密码--》对话框  取消/确定按钮 com.uc56.ucexpressbao:id/btn_neg   com.uc56.ucexpressbao:id/btn_pos
# driver.find_element_by_id("com.uc56.ucexpressbao:id/btn_pos").click() #确定
# sleep(1);
#登陆界面--》注册按钮com.uc56.ucexpressbao:id/register
driver.find_element_by_id("com.uc56.ucexpressbao:id/register").click()
sleep(1);
#注册界面--》注册 com.uc56.ucexpressbao:id/register_device  返回 com.uc56.ucexpressbao:id/img_left
driver.find_element_by_id("com.uc56.ucexpressbao:id/register_device").click()
sleep(3);
driver.find_element_by_id("com.uc56.ucexpressbao:id/img_left").click()
sleep(1);
driver.quit()