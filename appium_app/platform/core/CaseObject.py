import re
import datetime
import os
from ThinkCore.TFile import *
from ThinkCore.TYaml import *
from ThinkCore.TLog import *
from ThinkCore.TExcel import *
from ThinkCore.TEmail import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
import time
import appium_app.platform.core.Executor as Executor

'''
# 基础案例对象
# 页面元素步骤
'''

__author__ = 'banketree'


class CaseObject:
    caseInfo = None
    stepsInfos = []  # 每步执行状态
    checkPointInfo = None  # 检测点数据
    checkPointStatus = False  # 默认检测点--》不通过
    logger = None
    yamlParam = None
    executor = None  # 执行者
    screenPath = ""

    # yaml
    # 执行步骤超时配置
    # 文件操作

    # 驱动（初始化数据）
    def __init__(self, logger, yamlParam):
        self.caseInfo = None
        self.stepsInfos = []  # 每步执行状态
        self.checkPointInfo = None  # 检测点数据
        self.checkPointStatus = False  # 默认检测点--》不通过
        self.logger = logger
        self.yamlParam = yamlParam
        self.executor = None

        if (self.yamlParam == None or self.yamlParam.case == None):
            if (self.yamlParam != None and self.yamlParam.yamlPath != None):
                self.logger.error(str(self.yamlParam.yamlPath) + "-->文件读取失败")
            else:
                self.logger.error("脚本文件读取失败")
            return

    def __del__(self):
        pass

    def run(self, executor, param):
        if (executor == None or isinstance(executor, Executor) == False):
            self.logger.error("未识别到执行者")
            return
        self.executor = executor;

        # 读取脚本信息
        try:
            self.logger.info("开始初始化案例信息")
            self.caseInfo = self.yamlParam.case["info"]
            self.logger.info("案例信息:" + str(self.caseInfo))
            self.runInfo(self.caseInfo)
        except Exception as e:
            self.logger.error("案例信息 error:" + str(e))
            return

        # 执行脚本步骤
        try:
            self.logger.info("开始初始化案例步骤")
            steps = self.yamlParam.case["steps"]
            for step in steps:
                self.runStep(step)
        except Exception as e:
            self.logger.error("案例步骤 error:" + str(e))
            self.shotScreen()
            self.logger.error("系统日志:" + self.executor.getLog())
            return

        # 执行检测点
        try:
            self.logger.info("开始案例检测点")
            self.runCheckPoint(self.yamlParam.case["checkpoint"])
        except Exception as e:
            self.logger.error("案例检测点 error:" + str(e))
            self.shotScreen()
            self.logger.error("系统日志:" + self.executor.getLog())
            return
        self.shotScreen()

    def getCaseInfo(self):  # 案例信息
        return self.caseInfo

    def getStepsInfos(self):  # 每步执行状态
        return self.stepsInfos

    def getCheckPointInfo(self):  # 获取检测点信息
        return self.checkPointInfo

    def getCheckPointStatus(self):  # 检测点
        return self.checkPointStatus

    def getCheckPointString(self):  # 检测点
        if (self.getCheckPointStatus()):
            return "通过"
        return "不通过"

    def shotScreen(self):
        try:
            path = self.logger.getFilePath()
            name = str(time.strftime('%Y%m%d%H%M%S', time.localtime())) + ".jpg"
            self.executor.shotScreen(path, name)
            self.screenPath = path + "//" + name
        except Exception as e:
            print(e)

    def getScreenPath(self):
        return self.screenPath

    # - id:
    # name:
    # description:
    def runInfo(self, info):
        sleep(1)
        if (("id" not in info) or ("name" not in info) or ("description" not in info)):
            raise Exception("案例信息参数不全！");
        pass

    # 执行步骤（读取yaml所有的数据）
    # - element
    # find: xpath
    # event: click
    # description:
    def runStep(self, step):
        sleep(3)
        if (("element" not in step) or ("find" not in step) or ("event" not in step)):
            raise Exception("案例步骤参数不全！");
        self.logger.info("执行步骤:" + str(step))

        if ("description" in step):
            self.stepsInfos.append(step["description"] + "\n")
        item = None;
        if (step["find"] == "class" or step["find"] == "xpaths"):
            item = self.executor.find(step["find"], step["element"], step["index"])
        else:
            item = self.executor.find(step["find"], step["element"])

        eventResult = False
        if ("params" not in step):
            eventResult = self.executor.event(item, step["event"])
        else:
            eventResult = self.executor.event(item, step["event"], step["params"], self.yamlParam)

        if (eventResult):  # 成功
            self.logger.info("执行步骤结果:成功")
        else:  # 失败
            if (item == None):
                raise Exception("案例步骤：元素" + str(step["element"]) + "未找到");
            raise Exception("案例步骤：元素" + str(step["element"]) + str(step["event"]) + "执行失败");
        pass

    # 检测点
    # - element
    # find: xpath
    # description:
    def runCheckPoint(self, checkpoint):
        if (("element" not in checkpoint) or ("find" not in checkpoint) or ("event" not in checkpoint)):
            raise Exception("案例检测点参数不全！");
        self.logger.info("案例检测点信息:" + str(checkpoint))
        if ("description" in checkpoint):
            self.checkPointInfo = checkpoint["description"]
        item = None;
        if (checkpoint["find"] == "class" or checkpoint["find"] == "xpaths"):
            item = self.executor.find(checkpoint["find"], checkpoint["element"], checkpoint["index"])
        else:
            item = self.executor.find(checkpoint["find"], checkpoint["element"])

        if ("params" not in checkpoint):
            self.checkPointStatus = self.executor.event(item, checkpoint["event"])
        else:
            self.checkPointStatus = self.executor.event(item, checkpoint["event"], checkpoint["params"], self.yamlParam)

        if (self.checkPointStatus):  # 成功
            self.logger.info("案例检测成功")
        else:  # 失败
            if (item == None):
                raise Exception("案例检测点：元素" + str(checkpoint["element"]) + "未找到");
            raise Exception("案例检测点：元素" + str(checkpoint["element"]) + str(checkpoint["event"]) + "执行失败");
        pass


if __name__ == '__main__':
    excel = None
    caseObject = None
    print("开始执行脚本")
