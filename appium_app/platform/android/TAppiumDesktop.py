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

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

find_id = "id"
find_ids = "ids"
find_xpath = "xpath"
find_xpaths = "xpaths"
find_class_name = "class_name"
find_css = "css"

event_click = "click"
event_swipeDown = "swipeDown"
event_swipeUp = "swipeUp"
event_swipeLeft = "swipeLeft"
event_swipeRight = "swipeRight"
event_setValue = "setValue"
event_getValue = "getValue"
event_message = "message"
event_adb = "adb"
event_press = "press"
event_keyevent = "keyevent"
event_sleep = "sleep"
event_toWebview = "toWebview"
event_toNative = "toNative"
event_equal = "equal"
event_exist = "exist"
event_back = "back"
timeout = 30


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
    # def __init__(self, desiredCaps):
    #     self.dirver = webdriver.Remote('http://localhost:4723/wd/hub', desiredCaps)
    #
    # def __init__(self, ip, desiredCaps):
    #     self.dirver = webdriver.Remote('http://' + ip + ':4723/wd/hub', desiredCaps)
    dirver = None
    def __init__(self, desiredCaps, ip="localhost", port="4723"):
        self.dirver = webdriver.Remote('http://' + ip + ':' + port + '/wd/hub', desiredCaps)

    def __del__(self):
        if (self.dirver != None):
            self.dirver.quit()
        self.dirver = None

    def getDirver(self):
        return self.dirver;

    # 查找元素--->find-->findtype:id/ids/xpath -->index
    def find(self, findType, findField, index=0):
        try:
            if (findType == find_id):  # id
                return WebDriverWait(self.getDirver(), timeout).until(lambda x: x.find_element_by_id(findField))
            elif (findType == find_ids):  # ids
                return WebDriverWait(self.getDirver(), timeout).until(lambda x: x.find_elements_by_id(findField))[
                    index]
            elif (findType == find_xpath):  # xpath
                return WebDriverWait(self.getDirver(), timeout).until(lambda x: x.find_element_by_xpath(findField))
            elif (findType == find_xpaths):  # xpaths
                return WebDriverWait(self.getDirver(), timeout).until(lambda x: x.find_elements_by_xpath(findField))[
                    index]
            elif (findType == find_class_name):  # class
                return WebDriverWait(self.getDirver(), timeout).until(
                    lambda x: x.find_element_by_class_name(findField))
            elif (findType == find_css):  # css
                return WebDriverWait(self.getDirver(), timeout).until(
                    lambda x: x.find_element_by_css_selector(findField))
        except selenium.common.exceptions.TimeoutException:  # 超时
            return None
        except selenium.common.exceptions.NoSuchElementException:  # 不存在
            return None
        except Exception as e:
            print(e)
            return None

    def event(self, element, eventType="click", params=None):
        try:
            if (eventType == event_click):  # 点击事件
                element.click();
            elif (eventType == event_swipeDown):
                self.swipeToDown()
            elif (eventType == event_swipeUp):
                self.swipeToUp()
            elif (eventType == event_swipeLeft):
                self.swipeToLeft()
            elif (eventType == event_swipeRight):
                self.swipeToRight()
            elif (eventType == event_setValue):  # 赋值 事件 value
                if (params == None or 'value' not in params):
                    self.setValue("")
                    return True
                if ('clear' in params):
                    self.clearValue(element, params["clear"])
                self.setValue(element, str(params['value']))
            elif (eventType == event_getValue):
                pass
            elif (eventType == event_message):
                pass
            elif (eventType == event_adb):  # cmd 事件
                adb = TAdb()
                adb.sendCommand(params["cmd"])
                del adb
            elif (eventType == event_press):  # code 事件
                self.getDirver().press_keycode(params["code"])
            elif (eventType == event_keyevent):  # keyevent 事件
                self.getDirver().keyevent(params["code"])
            elif (eventType == event_sleep):  # 睡眠 second
                sleep(params["second"])
            elif (eventType == event_toWebview):  # 切换-->webview
                self.toWebview()
            elif (eventType == event_toNative):  # 切换--> native
                self.getDirver().switch_to.context("NATIVE_APP")
            elif (eventType == event_equal):  # 是否相等
                if (params == None or 'value' not in params):
                    return False
                if (self.getValue(element) == str(params['value'])):
                    return True
                return False
            elif (eventType == event_exist):  # 是否存在
                if (element != None):
                    return True
                return False
            elif (eventType == event_back):  # 回退
                self.getDirver().press_keycode(params['code'])
                return False
            pass
        except Exception as e:
            print(e)
            return False
        return True

    # 查找弹窗元素
    def isToastShow(self, xpath):
        try:
            WebDriverWait(self.getDirver(), 10, 0.5).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            return True
        except selenium.common.exceptions.TimeoutException:
            return False
        except selenium.common.exceptions.NoSuchElementException:
            return False
        except Exception:
            return False

    def toWebview(self):
        n = 1
        while n < 10:
            time.sleep(3)
            n = n + 1
            print(self.getDirver().contexts)
            for cons in self.getDirver().contexts:
                if cons.lower().startswith("webview"):
                    self.getDirver().switch_to.context(cons)
                    print("---切换webview---")
                    # print(self.getDirver().page_source)
                    self.getDirver().execute_script('document.querySelectorAll("head")[0].style.display="block"')
                    self.getDirver().execute_script('document.querySelectorAll("title")[0].style.display="block"')
                    return

    # 向左滑动  --》
    def swipeToLeft(self):
        width = self.getDirver().get_window_size()["width"]
        height = self.getDirver().get_window_size()["height"]
        x1 = int(width * 0.75)
        y1 = int(height * 0.5)
        x2 = int(width * 0.05)
        self.getDirver().swipe(x1, y1, x2, y1, 600)

    # 向右滑动 《--
    def swipeToRight(self):
        height = self.getDirver().get_window_size()["height"]
        width = self.getDirver().get_window_size()["width"]
        x1 = int(width * 0.05)
        y1 = int(height * 0.5)
        x2 = int(width * 0.75)
        self.getDirver().swipe(x1, y1, x1, x2, 1000)
        # self.getDirver().swipe(0, 1327, 500, 900, 1000)
        print("--swipeToUp--")

    # 向下滑动
    # swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000 从200滑动到400
    def swipeToDown(self):
        height = self.getDirver().get_window_size()["height"]
        x1 = int(self.getDirver().get_window_size()["width"] * 0.5)
        y1 = int(height * 0.25)
        y2 = int(height * 0.75)
        self.getDirver().swipe(x1, y1, x1, y2, 1000)
        # self.getDirver().swipe(0, 1327, 500, 900, 1000)
        print("--swipeToDown--")

    def swipeToUp(self):
        height = self.getDirver().get_window_size()["height"]
        width = self.getDirver().get_window_size()["width"]
        self.getDirver().swipe(width / 2, height * 3 / 4, width / 2, height / 4)
        # for i in range(n):
        #     self.getDirver().swipe(540, 800, 540, 560, 0)
        #     time.sleep(2)

    def clearValue(self, element, clearNum=0):
        if (element == None):
            return
        element.send_keys("")
        strLen = len(self.getValue(element));
        if (strLen > clearNum):
            clearNum = strLen;
        if (clearNum == 0):
            return
        self.getDirver().press_keycode(123)  # 光标移动到输入框最右边
        for n in range(0, clearNum):
            self.getDirver().keyevent(67)  # 删除

    def setValue(self, element, value):
        try:  # 数据一样者不赋值
            if (self.getValue(element) == value):
                return
            elif (self.getWebValue(element) == value):
                return
        except Exception:
            pass
        self.clearText(value)
        element.send_keys(value)
        self.hideSoftinput()

    def getValue(self, element):
        result = element.get_attribute("text")
        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)  # 只匹配中文，大小写，字母
        return "".join(re_reulst)

    def getWebValue(self, element):
        result = element.text
        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return "".join(re_reulst)

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
            self.getDirver().get_screenshot_as_file(os.path.join(screenshotPath + filename))
        except Exception:
            pass

    # 隐藏软盘
    def hideSoftinput(self):
        if (self.getDirver() == None):
            return

        adb = TAdb()
        try:
            if (adb.isSoftinputShown()):
                self.getDirver().hide_keyboard()
        except Exception as e:
            print(e)
            self.getDirver().press_keycode(4)  # KEYCODE_BACK 返回键
        del adb  #


if __name__ == "__main__":
    pass
