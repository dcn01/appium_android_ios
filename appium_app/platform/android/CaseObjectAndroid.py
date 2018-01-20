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
from appium_app.platform.core.CaseObject import *

'''
# 基础案例对象
# 页面元素步骤
'''

__author__ = 'banketree'


# android 测试用例
class CaseObjectAndroid(CaseObject):
    logger = None
    appiumDesktop = None  # 驱动
    yamlParam = None  # 参数

    def __init__(self, dirPath, yamlPath, param=None):
        self.logger = TLog(dirPath, "" + time.strftime('%Y%m%d%H%M%S', time.localtime()))
        super().__init__(self.logger, yamlPath)

    def __del__(self):
        super().__del__()
        if (self.appiumDesktop != None):
            del self.appiumDesktop
        if (self.logger != None):
            del self.logger

    def run(self):
        super().run(self.appiumDesktop)

    def getExecutor(self, desiredCaps, ip="localhost", port="4723"):
        if (self.appiumDesktop != None):
            return self.appiumDesktop;
        try:
            self.logger.info(u"开始初始化appium client ip:" + ip + " port:" + port)
            self.appiumDesktop = TAppiumDesktop(desiredCaps, ip, port);  # 设备连接属性
            return self.appiumDesktop
        except Exception as e:
            self.logger.error(u"appium client error:" + str(e))
        return None

    def getLogName(self):
        return self.logger.getFileName()


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
        loginCaseOutPath = (
            r"D:\Project\Python_Project\TestFramework\file\login\\" + str(time.strftime('%Y%m%d%H%M%S', startTime)));

        print("启动真机或模拟器")
        # 开始
        caseObject = CaseObjectAndroid(
            r"D:\Project\Python_Project\TestFramework\appium_app\case\login\login_xpath.yaml", loginCaseOutPath,
            desiredCaps)
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
