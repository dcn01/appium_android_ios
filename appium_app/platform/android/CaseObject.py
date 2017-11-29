import re

import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

__author__ = 'shikun'
# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
import time

'''
# 基础案例对象
# 查找元素、页面元素事件
'''

find_element_by_id = "id"
find_elements_by_id = "ids"
find_element_by_xpath = "xpath"
find_elements_by_xpath = "xpaths"
find_element_by_class_name = "class_name"
find_element_by_css_selector = "css"
timeout = 10

class CaseObject:
    # 驱动
    def __init__(self, driver):
        self.driver = driver

    # 查找元素--->find-->findtype:id/ids/xpath -->index
    def find(self,findType,findField,index=0):
        try:
            if( findType == find_element_by_id):#id
                return  WebDriverWait(self.driver, timeout).until(lambda x:self.driver.find_element_by_id(findField))
            elif( findType == find_elements_by_id):#ids
                return WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_elements_by_id(findField))[index]
            elif (findType == find_element_by_xpath):#xpath
                return WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_element_by_xpath(findField))
            elif (findType == find_elements_by_xpath):#xpaths
                return WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_elements_by_xpath(findField))[index]
            elif (findType == find_element_by_class_name):#class
                return WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_element_by_class_name(findField))
            elif (findType == find_element_by_css_selector):#css
                return WebDriverWait(self.driver, timeout).until(lambda x: self.driver.find_element_by_css_selector(findField))
        except selenium.common.exceptions.TimeoutException:
            # print("查找元素" + mOperate["element_info"] + "超时")
            return None
        except selenium.common.exceptions.NoSuchElementException:
            # print("查找元素" + mOperate["element_info"] + "不存在")
            return None
        except Exception:
            return None
        '''
        查找元素.mOperate,dict|list
        operate_type：对应的操作
        element_info：元素详情
        find_type: find类型
        '''
        try:
            if type(mOperate) == list:  # 多检查点
                for item in mOperate:
                    if item.get("is_webview", "0") == 1:  # 1表示切换到webview
                        self.switchToWebview()
                    elif item.get("is_webview", "0") == 2:
                        self.switchToNative()
                    t = item["check_time"] if item.get("check_time", "0") != "0" else be.WAIT_TIME
                    WebDriverWait(self.driver, t).until(lambda x: self.elements_by(item))
                return True
            if type(mOperate) == dict:  # 单检查点
                if mOperate.get("is_webview", "0") == 1:  # 1表示切换到webview
                    self.switchToWebview()

                elif mOperate.get("is_webview", "0") == 2:
                    self.switchToNative()

                if mOperate.get("element_info", "0") == "0":  # 如果没有页面元素，就不检测是页面元素，可能是滑动等操作
                    return True
                t = mOperate["check_time"] if mOperate.get("check_time",
                                                           "0") != "0" else be.WAIT_TIME  # 如果自定义检测时间为空，就用默认的检测等待时间
                WebDriverWait(self.driver, t).until(lambda x: self.elements_by(mOperate))  # 操作元素是否存在
                return True
        except selenium.common.exceptions.TimeoutException:
            # print("查找元素" + mOperate["element_info"] + "超时")
            return False
        except selenium.common.exceptions.NoSuchElementException:
            # print("查找元素" + mOperate["element_info"] + "不存在")
            return False


class OperateElement:
    def __init__(self, driver=""):
        self.driver = driver

    def findElement(self, mOperate):
        '''
        查找元素.mOperate,dict|list
        operate_type：对应的操作
        element_info：元素详情
        find_type: find类型
        '''
        try:
            if type(mOperate) == list:  # 多检查点
                for item in mOperate:
                    if item.get("is_webview", "0") == 1:  # 1表示切换到webview
                        self.switchToWebview()
                    elif item.get("is_webview", "0") == 2:
                        self.switchToNative()
                    t = item["check_time"] if item.get("check_time", "0") != "0" else be.WAIT_TIME
                    WebDriverWait(self.driver, t).until(lambda x: self.elements_by(item))
                return True
            if type(mOperate) == dict:  # 单检查点
                if mOperate.get("is_webview", "0") == 1:  # 1表示切换到webview
                    self.switchToWebview()

                elif mOperate.get("is_webview", "0") == 2:
                    self.switchToNative()

                if mOperate.get("element_info", "0") == "0":  # 如果没有页面元素，就不检测是页面元素，可能是滑动等操作
                    return True
                t = mOperate["check_time"] if mOperate.get("check_time",
                                                           "0") != "0" else be.WAIT_TIME  # 如果自定义检测时间为空，就用默认的检测等待时间
                WebDriverWait(self.driver, t).until(lambda x: self.elements_by(mOperate))  # 操作元素是否存在
                return True
        except selenium.common.exceptions.TimeoutException:
            # print("查找元素" + mOperate["element_info"] + "超时")
            return False
        except selenium.common.exceptions.NoSuchElementException:
            # print("查找元素" + mOperate["element_info"] + "不存在")
            return False

    '''
   查找元素.mOperate是字典
   operate_type：对应的操作
   element_info：元素详情
   find_type: find类型
   
   testInfo
   logTest: 记录日志
    '''

    def operate(self, mOperate, testInfo, logTest):
        try:
            if self.findElement(mOperate):
                info = ""
                if mOperate.get("element_info", "0") != "0":
                    info = mOperate["element_info"] + "_" + mOperate.get("operate_type", " ")
                elif mOperate.get("swipe", "0") != "0":
                    info = mOperate["swipe"]
                elif mOperate.get("press_keycode", "0") != "0":
                    info = "输入keycode=" + str(mOperate["press_keycode"])

                logTest.buildStartLine(testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + info)  # 记录日志

                if mOperate.get("swipe", "0") == be.SWIPE_DOWN:  # 向下滑动
                    self.swipeToDown()
                    return True
                if mOperate.get("swipe", "0") == be.SWIPE_UP:  # 向下滑动
                    self.swipeToUp()
                    return True

                if mOperate.get("press_keycode", "0") != "0":  # 键盘事件
                    self.press_keycode(mOperate["press_keycode"])

                if mOperate.get("operate_type", "0") == "0":  # 如果没有此字段，说明没有相应操作，直接返回
                    return True

                if mOperate["operate_type"] == be.CLICK:
                    self.click(mOperate)
                    return True

                if mOperate.get("is_webview", "0") == 1 and mOperate["operate_type"] == be.GET_VALUE:
                    return self.get_web_value(mOperate)

                if mOperate["operate_type"] == be.GET_VALUE:
                    return self.get_value(mOperate)

                if mOperate["operate_type"] == be.SET_VALUE:
                    self.set_value(mOperate)
                    return True
                if mOperate["operate_type"] == be.ADB_TAP:  # adb shell tap模拟触屏
                    # location
                    self.adb_tap(mOperate)
                    return True

                return True
            else:
                return False
        except IndexError:
            logTest.buildStartLine(
                testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + mOperate["element_info"] + "索引错误")  # 记录日志
            print(mOperate["element_info"] + "索引错误")
            return False

    def adb_tap(self, mOperate):

        bounds = self.elements_by(mOperate).location
        x = str(bounds["x"])
        y = str(bounds["y"])

        os.system("adb shell input tap " + x + " " + y)


