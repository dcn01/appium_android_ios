# coding=utf-8
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
from appium_app.platform.android.TAdb import *


def waitForElement(driver, idString, timeOut):
    second = 0
    while True:
        sleep(1)
        try:
            element = driver.find_element_by_id(idString)
            if (element != None):
                return element
        except Exception as e:
            print("not find " + idString)
        second += 1
        if (second >= timeOut):
            print("未找到元素")
            return None


def clearText(element):
    if (element == None):
        return
    text = element.__getattribute__("text")
    if (len(text) <= 0):
        return
    element.send_keys("")
    sleep(1)
    text = element.__getattribute__("text")
    if (len(text) <= 0):
        return
    driver.press_keycode(123)  # 光标移动到输入框最右边
    for i in range(0, len(text)):
        sleep(1)
        driver.keyevent(67)  # 删除


def fastInput(element, value):
    '快速输入'
    x = subprocess.check_output('adb devices', shell=True).split('\n')[1][:-7]
    element.click()
    sleep(0.3)
    subprocess.Popen('adb -s %s shell input text %s' % (x, str), shell=True)
    sleep(0.5)


def hideSoftinput():
    if (driver == None):
        return
    try:
        driver.hide_keyboard()
    except Exception as e:
        print(e)
        driver.keyevent(4)  # 返回键
        # driver.press_keycode(4)  # 返回键
    finally:
        sleep(1.5)

def setValue(element, value):
    if (element == None):
        return
    try:
        clearText(element)
        # driver.set_value(element,value)
        element.send_keys(value)
    except Exception as e:
        print(e)
    finally:
        # hideSoftinput();
        sleep(2)


devices = TAdb().getAttachedDevices()
phoneInfo = TAdb().getPhoneInfo(devices[0])

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = phoneInfo['system-realease']  # '7.1.1'
desired_caps['deviceName'] = phoneInfo['device']  # 'Test26'
# UC56
desired_caps['appPackage'] = 'com.uc56.ucexpressbao'
desired_caps['appActivity'] = '.activitys.SplashActivity'

desired_caps['unicodeKeyboard'] = True  # 使用unicodeKeyboard的编码方式来发送字符串
desired_caps['resetKeyboard'] = True  # 将键盘给隐藏起来
desired_caps['noReset'] = True  #不重新安装
# desired_caps['udid'] = True  #应用app进程标识
# desired_caps['wdaLocalPort'] = "8001"  #默认端口转发 8100

second = 1;
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
sleep(second)
# 手机号码
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("phone_num"))
# waitForElement(driver, "com.uc56.ucexpressbao:id/phone_num", 10)
setValue(element, '18221851560')
element = None
# 网点编号
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("web_id"))
setValue(element, '02017')
element = None
# 员工编号
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("employee_id"))
setValue(element, '00012800')
element = None
# 员工密码
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("password"))
setValue(element, '1111111111')
element = None
# hideSoftinput()
sleep(6)
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("save_password"))
if element!=None:
    element.click()

element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("save_password"))
if element!=None:
    element.click()

element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("login_button"))
if element!=None:
    element.click()
sleep(second);

# 忘记密码com.uc56.ucexpressbao:id/forget_password
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("forget_password"))
if element!=None:
    element.click()  # 是否重置密码

# 忘记密码--》对话框  取消/确定按钮 com.uc56.ucexpressbao:id/btn_neg   com.uc56.ucexpressbao:id/btn_pos
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("btn_pos"))
if element!=None:
    element.click()  # 确定

# 登陆界面--》注册按钮com.uc56.ucexpressbao:id/register
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("register"))
if element!=None:
    element.click()

# 注册界面--》注册 com.uc56.ucexpressbao:id/register_device  返回 com.uc56.ucexpressbao:id/img_left
element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("register_device"))
if element!=None:
    element.click()

# driver.get_screenshot_as_png()
# element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("img_left"))
# if element!=None:
#     element.click()

element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("password"))
setValue(element, '111111111')
element = None

element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("login_button"))
if element!=None:
    element.click()
sleep(second)
driver.quit()
