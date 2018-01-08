import re
import datetime
import os
from ThinkCore.TFile import *
from ThinkCore.TYaml import *
from ThinkCore.TLog import *
from ThinkCore.TExcel import *
from ThinkCore.TEmail import *
from appium_app.platform.android.TAppiumDesktop import *
from appium_app.platform.android.TAapt import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
import time

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
    file = None
    tyaml = None
    yaml = None
    adb = None

    # yaml
    # 执行步骤超时配置
    # 文件操作

    # 驱动（初始化数据）
    def __init__(self, appiumDesktop, yamlPath, logger):
        self.caseInfo = None
        self.stepsInfos = []  # 每步执行状态
        self.checkPointInfo = None  # 检测点数据
        self.checkPointStatus = False  # 默认检测点--》不通过
        self.logger = logger
        self.adb = TAdb()
        self.picture = ""

        self.appiumDesktop = appiumDesktop;
        self.file = TFile(yamlPath)
        if (self.file.existFile() == False):
            self.logger.error(str(yamlPath) + "---》文件不存在")
            return
        self.tyaml = TYaml()
        self.yaml = self.tyaml.getYam(yamlPath)
        if (self.yaml == None):
            self.logger.error(str(yamlPath) + "---》文件读取失败")
            return
        try:
            self.logger.info("开始初始化案例信息")
            self.caseInfo = self.yaml["info"]
            self.logger.info("案例信息:" + str(self.caseInfo))
            self.runInfo(self.caseInfo)
        except Exception as e:
            self.logger.error("案例信息 error:" + str(e))
            return

        try:
            self.logger.info("开始初始化案例步骤")
            steps = self.yaml["steps"]
            for step in steps:
                self.runStep(step)
        except Exception as e:
            self.logger.error("案例步骤 error:" + str(e))
            self.saveScreen()
            self.logger.error("日志:" + self.adb.getLog())
            return

        try:
            self.logger.info("开始案例检测点")
            self.runCheckPoint(self.yaml["checkpoint"])
        except Exception as e:
            self.logger.error("案例检测点 error:" + str(e))
            self.saveScreen()
            self.logger.error("日志:" + self.adb.getLog())
            return
        self.saveScreen()

    def __del__(self):
        if (self.file != None):
            del self.file;
        if (self.yaml != None):
            del self.yaml;
        if (self.tyaml != None):
            del self.tyaml;
        if (self.adb != None):
            del self.adb;

    def saveScreen(self):
        try:
            path = self.logger.getFilePath()
            name = str(time.strftime('%Y%m%d%H%M%S', time.localtime())) + ".jpg"
            self.appiumDesktop.shotScreen(path, name)
            self.picture = path + "//" + name
        except Exception as e:
            print(e)

    def getPicture(self):
        return self.picture

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
            item = self.appiumDesktop.find(step["find"], step["element"], step["index"])
        else:
            item = self.appiumDesktop.find(step["find"], step["element"])

        if (item == None):
            raise Exception("案例步骤：元素" + str(step["element"]) + "未找到");

        eventResult = False
        if ("params" not in step):
            eventResult = self.appiumDesktop.event(item, step["event"])
        else:
            eventResult = self.appiumDesktop.event(item, step["event"], step["params"])

        if (eventResult):  # 成功
            self.logger.info("执行步骤结果:成功")
        else:  # 失败
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
            item = self.appiumDesktop.find(checkpoint["find"], checkpoint["element"], checkpoint["index"])
        else:
            item = self.appiumDesktop.find(checkpoint["find"], checkpoint["element"])

        if (item == None):
            raise Exception("案例检测点：元素" + str(checkpoint["element"]) + "未找到");

        if ("params" not in checkpoint):
            self.checkPointStatus = self.appiumDesktop.event(item, checkpoint["event"])
        else:
            self.checkPointStatus = self.appiumDesktop.event(item, checkpoint["event"], checkpoint["params"])

        if (self.checkPointStatus):  # 成功
            self.logger.info("案例检测成功")
        else:  # 失败
            raise Exception("案例检测点：元素" + str(checkpoint["element"]) + str(checkpoint["event"]) + "执行失败");
        pass


# android 测试用例
class CaseObjectAndroid(CaseObject):
    logger = None
    appiumDesktop = None

    def __init__(self, yamlPath, dirPath, desiredCaps, ip="localhost", port="4723"):
        self.logger = TLog(dirPath, "" + time.strftime('%Y%m%d%H%M%S', time.localtime()))
        try:
            self.logger.info(u"开始初始化appium client ip:" + ip + " port:" + port)
            self.appiumDesktop = TAppiumDesktop(desiredCaps, ip, port);  # 设备连接属性
        except Exception as e:
            self.logger.error(u"appium client error:" + str(e))
            return
        super().__init__(self.appiumDesktop, yamlPath, self.logger)

    def __del__(self):
        super().__del__()
        if (self.appiumDesktop != None):
            del self.appiumDesktop
        if (self.logger != None):
            del self.logger

    def getLogName(self):
        return self.logger.getFileName()


# ios 测试用例
class CaseObjectIos(CaseObject):
    pass


if __name__ == '__main__':
    excel = None
    caseObject = None
    print("开始执行脚本")
    adb = TAdb();
    try:
        adb.startServer()
        devices = adb.getAttachedDevices()
        if (len(devices) <= 0):
            raise Exception("未检测到设备")
        phoneInfo = TAdb().getPhoneInfo(devices[0])

        desiredCaps = {}
        desiredCaps['platformName'] = 'Android'
        desiredCaps['platformVersion'] = phoneInfo['system-realease']  # '7.1.1'
        desiredCaps['deviceName'] = phoneInfo['device']  # 'Test26'
        desiredCaps['app'] = r"D:\Project\Python_Project\TestFramework\file\app-sit3.0.1A2017-12-2618.apk"
        desiredCaps['appPackage'] = 'com.uc56.ucexpressbao'
        desiredCaps['appActivity'] = '.activitys.SplashActivity'
        desiredCaps['resetKeyboard'] = True  # 将键盘给隐藏起来9
        desiredCaps['noReset'] = True  # 不重新安装
        desiredCaps['udid'] = devices[0]  # 应用app进程标识
        # desiredCaps['wdaLocalPort'] = "8001"  # 默认端口转发 8100
        # appiumDesktop = TAppiumDesktop(desiredCaps);  # 设备连接属性
        startTime = time.localtime()
        startDate = datetime.datetime.now()
        loginCaseOutPath = (r"D:\Project\Python_Project\TestFramework\file\login\\" + str(time.strftime('%Y%m%d%H%M%S', startTime)));

        print("启动真机或模拟器")
        # 开始
        caseObject = CaseObjectAndroid(r"D:\Project\Python_Project\TestFramework\appium_app\case\login\login_xpath.yaml",loginCaseOutPath, desiredCaps)
        # 结束
        endDate = datetime.datetime.now()
        print("执行完毕,正在统计数据")
        excelOutFilePath = loginCaseOutPath + '\\report.xlsx'
        excel = TExcel(excelOutFilePath, u"测试总况", u"测试详情")

        casePass = 0
        caseFail = 0
        caseNum = 0

        if (caseObject.getCheckPointStatus()):
            casePass += 1
            caseNum += 1
        else:
            caseFail += 1
            caseNum += 1

        apk = TAapk(r"D:\Project\Python_Project\TestFramework\file\app-sit3.0.1A2017-12-2618.apk")
        sum = {'testSumDate': str((endDate - startDate).seconds) + '秒', 'sum': caseNum, 'pass': casePass,
               'testDate': str(time.strftime('%Y-%m-%d %H-%M-%S', startTime)),
               'fail': caseFail,
               'appVersion': apk.getApkVersionName(), 'appSize': apk.getApkSize(), 'appName': apk.getApkName()}
        excel.initStatisticsData(sum)

        caseInfo = caseObject.getCaseInfo()
        checkPointInfo = caseObject.getCheckPointInfo()
        info = {"phoneClass": phoneInfo["brand"], "id": caseInfo["id"], "caseName": caseInfo["name"],
                "caseDescription": str(caseInfo["description"]), "caseFunction": "无",
                "precondition": "无", "step": str(caseObject.getStepsInfos()), "checkpoint": str(checkPointInfo),
                "result": str(caseObject.getCheckPointString()), "remarks": "日志名:" + str(caseObject.getLogName()),
                "screenshot": "无"}
        excel.initDetailData(info)
        excel.close()
        print("统计数据完毕,正在发送邮箱…")
        email = TEmail(r"D:\Project\Python_Project\TestFramework\email.ini")
        email.sendMail(excelOutFilePath)
        print("发送邮箱完毕")
    except Exception as ex:
        print(ex)
    finally:
        if (adb != None):
            del adb;
        if (caseObject != None):
            del caseObject
        if (excel != None):
            del excel
