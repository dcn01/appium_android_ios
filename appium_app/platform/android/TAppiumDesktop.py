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
from appium_app.platform.android.TAppiumServer import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

find_element_by_id = "id"
find_elements_by_id = "ids"
find_element_by_xpath = "xpath"
find_elements_by_xpath = "xpaths"
find_element_by_class_name = "class_name"
find_element_by_css_selector = "css"
timeout = 10


def waitForElement(driver, idString):
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
        if (second >= timeout):
            print("未找到元素")
            return None


# android驱动
class TAppiumDesktop(TAppiumServer):
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

    # 查找元素--->find-->findtype:id/ids/xpath -->index
    def find(self, findType, findField, index=0):
        try:
            if (findType == find_element_by_id):  # id
                return WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_element_by_id(findField))
            elif (findType == find_elements_by_id):  # ids
                return WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_elements_by_id(findField))[
                    index]
            elif (findType == find_element_by_xpath):  # xpath
                return WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_element_by_xpath(findField))
            elif (findType == find_elements_by_xpath):  # xpaths
                return \
                    WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_elements_by_xpath(findField))[
                        index]
            elif (findType == find_element_by_class_name):  # class
                return WebDriverWait(self.driver, timeout).until(
                    lambda x: self.driver.find_element_by_class_name(findField))
            elif (findType == find_element_by_css_selector):  # css
                return WebDriverWait(self.driver, timeout).until(
                    lambda x: self.driver.find_element_by_css_selector(findField))
        except selenium.common.exceptions.TimeoutException:  # 超时
            return None
        except selenium.common.exceptions.NoSuchElementException:  # 不存在
            return None
        except Exception:
            return None

    # 查找弹窗元素
    def isToastShow(self, xpath):
        try:
            WebDriverWait(self.driver, 10, 0.5).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            return True
        except selenium.common.exceptions.TimeoutException:
            return False
        except selenium.common.exceptions.NoSuchElementException:
            return False
        except Exception:
            return False

    # 点击事件
    def click(self, element):
        try:
            element.click();
        except Exception:
            pass

    # code 事件
    def pressKeycode(self, code):
        try:
            self.driver.press_keycode(code)
        except Exception:
            pass

    # code 事件
    def keyevent(self, code):
        try:
            self.driver.keyevent(code)
        except Exception:
            pass

    # 切换--> native
    def switchToNative(self):
        try:
            self.driver.switch_to.context("NATIVE_APP")
        except Exception:
            pass

    # 切换-->webview
    def switchToWebview(self):
        try:
            n = 1
            while n < 10:
                time.sleep(3)
                n = n + 1
                print(self.driver.contexts)
                for cons in self.driver.contexts:
                    if cons.lower().startswith("webview"):
                        self.driver.switch_to.context(cons)
                        print("---切换webview---")
                        # print(self.driver.page_source)
                        self.driver.execute_script('document.querySelectorAll("head")[0].style.display="block"')
                        self.driver.execute_script('document.querySelectorAll("title")[0].style.display="block"')
                        return
        except Exception:
            pass

    # 向左滑动  --》
    def swipeToLeft(self):
        try:
            width = self.driver.get_window_size()["width"]
            height = self.driver.get_window_size()["height"]
            x1 = int(width * 0.75)
            y1 = int(height * 0.5)
            x2 = int(width * 0.05)
            self.driver(x1, y1, x2, y1, 600)
        except Exception:
            pass

    # 向右滑动 《--
    def swipeToRight(self):
        try:
            height = self.driver.get_window_size()["height"]
            width = self.driver.get_window_size()["width"]
            x1 = int(width * 0.05)
            y1 = int(height * 0.5)
            x2 = int(width * 0.75)
            self.driver.swipe(x1, y1, x1, x2, 1000)
            # self.driver.swipe(0, 1327, 500, 900, 1000)
            print("--swipeToUp--")
        except Exception:
            pass

    # 向下滑动
    # swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000 从200滑动到400
    def swipeToDown(self):
        try:
            height = self.driver.get_window_size()["height"]
            x1 = int(self.driver.get_window_size()["width"] * 0.5)
            y1 = int(height * 0.25)
            y2 = int(height * 0.75)
            self.driver.swipe(x1, y1, x1, y2, 1000)
            # self.driver.swipe(0, 1327, 500, 900, 1000)
            print("--swipeToDown--")
        except Exception:
            pass

    def swipeToUp(self):
        try:
            height = self.driver.get_window_size()["height"]
            width = self.driver.get_window_size()["width"]
            self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4)
            # for i in range(n):
            #     self.driver.swipe(540, 800, 540, 560, 0)
            #     time.sleep(2)
        except Exception:
            pass

    def setValue(self, element, value):
        try:
            element.send_keys(value)
        except Exception:
            pass

    def getValue(self, element):
        try:
            result = element.get_attribute("text")
            re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)# 只匹配中文，大小写，字母
            return "".join(re_reulst)
        except Exception:
            pass

    def getWebValue(self, element):
        try:
            result = element.text
            re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
            return "".join(re_reulst)
        except Exception:
            pass

    # 清空文本
    def clearText(self, element):
        try:
            if (element == None):
                return
            text = self.getValue(element);
            if (len(text) <= 0):
                return
            element.send_keys("")
            sleep(1)
            text = self.getValue(element);
            if (len(text) <= 0):
                return
            self.pressKeycode(123)  # 光标移动到输入框最右边
            for i in range(0, len(text)):
                sleep(1)
                self.keyevent(67)  # 删除
        except Exception:
            pass

    # 截图
    def shotScreen(self, filePath, filename):
        try:
            screenshotPath = os.path.join(filePath, filename)
            if not os.path.exists(screenshotPath):
                os.makedirs(screenshotPath)
            sleep(1)
            self.driver.get_screenshot_as_file(os.path.join(screenshotPath + filename))
        except Exception:
            pass

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
