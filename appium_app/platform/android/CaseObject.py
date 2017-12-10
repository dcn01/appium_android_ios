import re

import os
from ThinkCore.TFile import *
from ThinkCore.TYaml import *
from appium_app.platform.android.TAppiumDesktop import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

__author__ = 'shikun'
# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
import time

'''
# 基础案例对象
# 页面元素步骤
'''


class CaseObject:
    # yaml
    # 执行步骤超时配置
    # 文件操作

    # 驱动（初始化数据）
    def __init__(self, yamlPath):
        self.file = TFile(yamlPath)
        if (self.file.existFile() == False):
            raise Exception(yamlPath + "---》文件不存在")
        self.tyaml = TYaml()
        self.yaml = self.tyaml.getYam(yamlPath)
        del self.tyaml
        if (self.yaml == None):
            raise Exception(yamlPath + "---》文件读取失败");
        self.runInfo(self.yaml["info"])
        self.steps = self.yaml["steps"]
        for step in self.steps:
            self.runStep(step)
        self.runCheckPoint(self.yaml["checkpoint"])

    def __del__(self):
        del self.file;
        del self.yaml;
        del self.tyaml;

    def runInfo(self, info):
        sleep(1)
        # - id:
        # name:
        # description:
        pass

    # 执行步骤（读取yaml所有的数据）
    def runStep(self, step):
        sleep(3)
        # - element
        # find: xpath
        # event: click
        # description:
        pass

    # 检测点
    def runCheckPoint(self, checkpoint):
        sleep(3)
        # - element
        # find: xpath
        # event: click
        # description:
        pass

# android 测试用例
class CaseObjectAndroid(CaseObject):
    def __init__(self, appiumDesktop, yamlPath):
        self.appiumDesktop = appiumDesktop;
        super().__init__(yamlPath)

    def __del__(self):
        super().__del__()

    def runInfo(self, info):  # 由父类回调
        super().runInfo(info)

    def runStep(self, step):  # 由父类回调
        super().runStep(step)
        if (("element" not in step) or ("find" not in step) or ("event" not in step)):
            return;

        item = None;
        if (step["find"] == "ids" or step["find"] == "xpaths"):
            item = self.appiumDesktop.find(step["find"], step["element"], step["index"])
        else:
            item = self.appiumDesktop.find(step["find"], step["element"])

        if (item == None):
            return;

        eventResult = False
        if ("params" not in step):
            eventResult = appiumDesktop.event(item, step["event"])
        else:
            eventResult = appiumDesktop.event(item, step["event"], step["params"])

        if (eventResult):  # 成功
            pass
        else:  # 失败
            pass

    def runCheckPoint(self, checkpoint):  # 由父类回调
        super().runCheckPoint(checkpoint)


# ios 测试用例
class CaseObjectIos(CaseObject):
    pass


if __name__ == '__main__':
    try:
        devices = TAdb().getAttachedDevices()
        if (len(devices) <= 0):
            raise Exception("未检测到设备")
        phoneInfo = TAdb().getPhoneInfo(devices[0])

        desiredCaps = {}
        desiredCaps['platformName'] = 'Android'
        desiredCaps['platformVersion'] = phoneInfo['system-realease']  # '7.1.1'
        desiredCaps['deviceName'] = phoneInfo['device']  # 'Test26'
        desiredCaps['app'] = r"D:\Project\Python_Project\TestFramework\file\app-sit2.8.2A2017-12-09-18.apk"
        desiredCaps['appPackage'] = 'com.uc56.ucexpressbao'
        desiredCaps['appActivity'] = '.activitys.SplashActivity'
        desiredCaps['resetKeyboard'] = True  # 将键盘给隐藏起来
        desiredCaps['noReset'] = True  # 不重新安装
        desiredCaps['udid'] = devices[0]  # 应用app进程标识
        # desiredCaps['wdaLocalPort'] = "8001"  # 默认端口转发 8100
        appiumDesktop = TAppiumDesktop(desiredCaps);  # 设备连接属性
        caseObject = CaseObjectAndroid(appiumDesktop,
                                       r"D:\Project\Python_Project\TestFramework\appium_app\case\login\login.yaml")
        print(caseObject);
    except Exception as ex:
        print(ex)
    finally:
        del appiumDesktop;
        del caseObject;
