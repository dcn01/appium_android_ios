# coding: utf-8
import multiprocessing
import time
import urllib
import unittest
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
from appium_app.platform.android.CaseObject import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
import time


class TestCaseRunner():

    def __init__(self, ymlPath, outPath, desiredCaps):
        self.ymlPath = ymlPath
        self.outPath = outPath
        self.desiredCaps = desiredCaps
        self.caseObject = None

    def __del__(self):
        if (caseObject != None):
            del self.caseObject

    def runCase(self):
        try:
            self.caseObject = CaseObjectAndroid(self.ymlPath, self.outPath, self.desiredCaps)
        except Exception as ex:
            print(ex)

    def getYmlPath(self):
        return self.ymlPath;

    def getCaseObject(self):
        return self.caseObject;


def func(apkPath, device, aapk):
    print("进程-" + str(os.getpid()) + "-执行开始")
    adb = TAdb();
    yamlCases = []
    startTime = time.localtime()
    startDate = datetime.datetime.now()

    try:
        caseOutPath = (r"D:\Project\Python_Project\TestFramework\file\\" + str(time.strftime('%Y%m%d%H%M%S', startTime)) + random.randint(0,99));
        phoneInfo = adb.getPhoneInfo(device)
        yamlCases.append(TestCaseRunner(r"D:\Project\Python_Project\TestFramework\appium_app\case\login\login_id.yaml",caseOutPath,getDesiredCaps(apkPath, device)))
        yamlCases.append(TestCaseRunner(r"D:\Project\Python_Project\TestFramework\appium_app\case\login\login_class.yaml",caseOutPath,getDesiredCaps(apkPath, device)))
        # yamlCases.append(TestCaseRunner(r"D:\Project\Python_Project\TestFramework\appium_app\case\login\login_xpath.yaml",caseOutPath,getDesiredCaps(apkPath, device)))
        # yamlCases.append(TestCaseRunner(r"D:\Project\Python_Project\TestFramework\appium_app\case\login\login_xpaths.yaml",caseOutPath,getDesiredCaps(apkPath, device)))
        # ……
        for case in yamlCases:
            try:
                case.runCase();
            except Exception as ex2:
                print(ex2)
    except Exception as ex:
        print(ex)
    finally:
        if (adb != None):
            del adb;

    # 开始统计结果
    # for case in cases:
    #     print(case.getPath())
    endDate = datetime.datetime.now()
    print("执行完毕,正在统计数据")
    excelOutFilePath = caseOutPath + '\\report.xlsx'
    excel = TExcel(excelOutFilePath, u"测试总况", u"测试详情")

    casePass = 0
    caseFail = 0
    caseNum = len(yamlCases)

    for case in yamlCases:
        caseObject = case.getCaseObject();
        if(caseObject==None):
            continue
        if (caseObject.getCheckPointStatus()):
            casePass += 1
        else:
            caseFail += 1

        caseInfo = caseObject.getCaseInfo()
        checkPointInfo = caseObject.getCheckPointInfo()
        picture = "无"
        if(caseObject.getPicture() != "" and TFile(caseObject.getPicture()).existFile()):
            picture = caseObject.getPicture();

        info = {"phoneClass": phoneInfo["brand"], "id": caseInfo["id"], "caseName": caseInfo["name"],
                "caseDescription": str(caseInfo["description"]), "caseFunction": "无",
                "precondition": "无", "step": str(caseObject.getStepsInfos()), "checkpoint": str(checkPointInfo),
                "result": str(caseObject.getCheckPointString()), "remarks": "日志名:" + str(caseObject.getLogName()),
                "screenshot": picture}
        excel.initDetailData(info)

    sum = {'testSumDate': str((endDate - startDate).seconds) + '秒', 'sum': caseNum, 'pass': casePass,
           'testDate': str(time.strftime('%Y-%m-%d %H-%M-%S', startTime)),
           'fail': caseFail,
           'appVersion': aapk.getApkVersionName(), 'appSize': aapk.getApkSize(), 'appName': aapk.getApkName()}
    excel.initStatisticsData(sum)

    excel.close()
    print("统计数据完毕,正在发送邮箱…")
    email = TEmail(r"D:\Project\Python_Project\TestFramework\email.ini")
    email.sendMail(excelOutFilePath)
    print("发送邮箱完毕")


    print("进程-" + str(os.getpid()) + "-执行结束")


def getDesiredCaps(apkPath, device):
    desiredCaps = {}
    adb =  TAdb();
    aapk = TAapk(apkPath)
    try:
        appPackage = aapk.getApkPackageName();
        appActivity = aapk.getApkActivity().strip();
        apkVersionName = aapk.getApkVersionName();
        appVersionName = adb.getAppVersionName(appPackage);

        phoneInfo = adb.getPhoneInfo(device)
        desiredCaps['platformName'] = 'Android'
        desiredCaps['platformVersion'] = phoneInfo['system-realease']  # '7.1.1'
        desiredCaps['deviceName'] = phoneInfo['device']  # 'Test26'
        desiredCaps['app'] = apkPath
        desiredCaps['appPackage'] = appPackage
        desiredCaps['appActivity'] = appActivity
        desiredCaps['resetKeyboard'] = True  # 将键盘给隐藏起来9
        desiredCaps['noReset'] = True  # 不重新安装
        desiredCaps['udid'] = device  # 应用app进程标识
        # desiredCaps['wdaLocalPort'] = "8001"  # 默认端口转发 8100
        if(apkVersionName != appVersionName):
            desiredCaps['noReset'] = False  # 重新安装
    except Exception as ex:
        print(ex);
    finally:
        del adb;
        del aapk;


    return desiredCaps;


def run(apkPath):
    print("执行脚本开始")
    pool = multiprocessing.Pool(processes=10)
    adb = TAdb();  #
    aapk = None;
    try:
        adb.startServer()
        devices = adb.getAttachedDevices()
        if (len(devices) <= 0):
            raise Exception("未检测到设备")
        aapk = TAapk(apkPath)
        for device in devices:
            pool.apply_async(func, (apkPath, device, aapk))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    except Exception as ex:
        print(ex)
    finally:
        if (adb != None):
            del adb;
        if (aapk != None):
            del aapk;
    pool.close()
    pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print("执行脚本結束")

if __name__ == "__main__":
    run(r"D:\Project\Python_Project\TestFramework\file\app-sit3.0.1A-2017-12-2716.apk")
