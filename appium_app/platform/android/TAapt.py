# coding=utf-8

import os
import re
import subprocess
from math import floor
import sys

from ThinkCore.TFile import *

'''
aapt 工具 读取apk文件的信息
'''


class TAapk():
    def __init__(self, apkPath):
        self.apkPath = apkPath
        self.fileException()

    def fileException(self):
        file = TFile(self.apkPath, "r")
        if file.existFile() == False:
            del file
            raise Exception('file not exists')
        del file

    # 得到app的文件大小
    def getApkSize(self):
        self.fileException()
        size = floor(os.path.getsize(self.apkPath) / (1024 * 1000))
        return str(size) + "M"

    def getApkInfo(self):
        self.fileException()
        # sys.setdefaultencoding('utf-8')
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        print(self.apkPath)
        match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output.decode())
        if not match:
            raise Exception("can't get packageinfo")
        packagename = match.group(1)
        versionCode = match.group(2)
        versionName = match.group(3)

        print('packagename:' + packagename)
        print('versionCode:' + versionCode)
        print('versionName:' + versionName)
        return packagename, versionName, versionCode

    def getApkPackageName(self):
        return self.getApkInfo()[0]

    def getApkVersionName(self):
        return self.getApkInfo()[1]

    def getApkVersionCode(self):
        return self.getApkInfo()[2]

    # 得到应用名字
    def getApkName(self):
        self.fileException()
        # sys.setdefaultencoding('utf-8')
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        t = output.decode().split()
        for item in t:
            # print(item)
            match = re.compile("application-label:(\S+)").search(item)
            if match is not None:
                return match.group(1)
        return ""

    # 得到启动类
    def getApkActivity(self):
        self.fileException()
        # sys.setdefaultencoding('utf-8')
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        match = re.compile("launchable-activity: name=(\S+)").search(output.decode())
        if match is not None:
            return match.group(1)
        return ""


if __name__ == '__main__':
    try:
        apk = TAapk(r"D:\Project\Python_Project\TestFramework\file\app-sit2.8.2A2017-12-09-18.apk")
        apk.getApkInfo()
        print(apk.getApkName())
        print(apk.getApkSize())
        print(apk.getApkActivity())

    except IOError:
        print("file not exsit")
