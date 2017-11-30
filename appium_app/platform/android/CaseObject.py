import re

import os
from ThinkCore.TFile import *
from ThinkCore.TYaml import *
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
        self.file = TFile()
        if (self.file.existFile(yamlPath) == False):
            raise Exception(yamlPath + "---》文件不存在")
        tyaml = TYaml()
        self.yaml = tyaml.getYam(yamlPath)
        if (self.yaml == None):
            raise Exception(yamlPath + "---》文件读取失败");

    def __del__(self):
        del self.file;

    # 执行步骤
    def runStep(self):
        pass

    # 检测点
    def checkPoint(self):
        pass


# android 测试用例
class CaseObjectAndroid(CaseObject):
    pass


# ios 测试用例
class CaseObjectIos(CaseObject):
    pass
