# -*- coding: utf-8 -*-
import os
import urllib
from multiprocessing import Process
import threading
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
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


# android驱动
class TDriver:
    # 参数要求
    # desired_caps = {}
    # desired_caps['platformName'] = 'Android'
    # desired_caps['platformVersion'] = phoneInfo['system-realease']  # '7.1.1'
    # desired_caps['deviceName'] = phoneInfo['device']  # 'Test26'
    # desired_caps['appPackage'] = 'com.uc56.ucexpressbao'
    # desired_caps['appActivity'] = '.activitys.SplashActivity'
    # desired_caps['resetKeyboard'] = True  # 将键盘给隐藏起来
    # desired_caps['noReset'] = True  # 不重新安装
    # desired_caps['udid'] = True  #应用app进程标识
    # desired_caps['wdaLocalPort'] = "8001"  #默认端口转发 8100
    def __init__(self, desiredCaps):
        self.dirver = webdriver.Remote('http://localhost:4723/wd/hub', desiredCaps)
        self.adb = TAdb()

    def __init__(self, ip, desiredCaps):
        self.dirver = webdriver.Remote('http://' + ip + ':4723/wd/hub', desiredCaps)
        self.adb = TAdb()

    def __init__(self, ip, port, desiredCaps):
        self.dirver = webdriver.Remote('http://' + ip + ':' + port + '/wd/hub', desiredCaps)
        self.adb = TAdb()

    def __del__(self):
        del self.adb;

    # 清空文本
    def clearText(self, element):
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
        self.driver.press_keycode(123)  # 光标移动到输入框最右边
        for i in range(0, len(text)):
            sleep(1)
            self.driver.keyevent(67)  # 删除

    # 截图
    def shotScreen(self, filePath, filename):
        screenshotPath = os.path.join(filePath, filename)
        if not os.path.exists(screenshotPath):
            os.makedirs(screenshotPath)
        sleep(1)
        self.driver.get_screenshot_as_file(os.path.join(screenshotPath + filename))

    # 隐藏软盘
    def hideSoftinput(self):
        if (self.driver == None):
            return
        try:
            if (self.adb.isSoftinputShown()):
                self.driver.hide_keyboard()
        except Exception as e:
            print(e)
            self.driver.keyevent(4)  # 返回键
        finally:
            sleep(1.5)


#
if __name__ == "__main__":
    pass
