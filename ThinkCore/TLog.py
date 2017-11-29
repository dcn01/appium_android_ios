# -*- coding: utf-8 -*-
import logging
import time
import os
from time import sleep
import threading
from appium_app.platform.android.TAdb import *
from appium_app.platform.android.TAppiumDesktop import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# 日志
class TLog:
    def __init__(self, pathDir, fileName):
        global logger, logPath,logName
        logPath = os.path.join(pathDir, fileName)
        logName = fileName
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        self.checkNo = 0
        self.logger = logging.getLogger()
        fh = logging.FileHandler(os.path.join(logPath, fileName + ".log"))
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    # 得到日志对象
    def getLog(self):
        return self.logger

    def getFilePath(self):
        return self.logPath

    def getFileName(self):
        return self.logName

    # 书写内容
    def info(self, result):
        self.logger.setLevel(logging.INFO)
        self.logger.info(result)

    def error(self, result):
        self.logger.error(result)

# if __name__ == "__main__":
#     logger = TLog(PATH(u"D:/Project/Python_Project/TestFramework/file"),
#                   "" + time.strftime('%Y%m%d%H%M%S', time.localtime()))
#     logger.info("sfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfgsfsdfsdfsdgdfgdfgdfghfghfg" + time.strftime('%Y%m%d%H%M%S', time.localtime()))
#     logger.error("          error" + time.strftime('%Y%m%d%H%M%S', time.localtime()))
#     del logger
    # adb = TAdb()
    # devicess = adb.getAttachedDevices()
    # if len(devicess) > 0:
    #     l_devices = []
    #     for devices in devicess:
    #         phoneInfo = TAdb().getPhoneInfo(devices)
    #         phoneName = "android" + "_" + phoneInfo["brand"] + "_" + phoneInfo["model"] + "_" + phoneInfo[
    #             "system-realease"] + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime())
    #         logger = TLog(PATH("../../../file"), "test2017-11-27")
    #         logger.info("sfsfsfsdfsdfsdfsdfgdfgdfg")
    #         # logger.info("log:" + adb.getBugReport())
    #         # logger.error("error2017-11-27")
    #         # logger.error("error")
    #         del logger
    # else:
    #     print("没有可用的安卓设备")
    # del adb
