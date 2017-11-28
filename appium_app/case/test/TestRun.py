# -*- coding:utf-8 -*-
from __future__ import division
import time
import datetime,subprocess
import unittest
import threading
from appium import webdriver
import os
import xlrd,xlwt,xlutils
from xlutils.copy import copy
# import wx
# from HTMLTestRunner import HTMLTestRunner
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.touch_action import TouchAction

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1.1'
desired_caps['deviceName'] = 'Test26'
#UC56
desired_caps['appPackage'] = 'com.uc56.ucexpressbao'
desired_caps['appActivity'] = '.activitys.SplashActivity'

# desired_caps["unicodeKeyboard"] = "True"
# desired_caps["resetKeyboard"] = "True"
subprocess.Popen('killall node',shell=True)
ipp = ['192.168.0.171','192.168.0.175']
tt = []   #多线程对象
def server(ip):
    for i in range(len(ip)):
        subprocess.Popen('/Applications/Appium.app/Contents/Resources/node/bin/node /Applications/Appium.app/Contents/Resources/node_modules/appium/build/lib/main.js --address "127.0.0.1" -p "'+str(4723+2*i)+'" --command-timeout "100"  --automation-name "Appium" -U "'+ip[i]+':'+str(5555+i)+'" >/tmp/1.txt',shell=True)
        time.sleep(3.5)
        wzj = webdriver.Remote('http://localhost:'+str(4723+2*i)+'/wd/hub', desired_caps)
        t = threading.Thread(target=DingWei().begin)
        tt.append(t)

class DingWei():
    def __init__(self):
        pass

    def begin(self):
        time.sleep(5)

if __name__ == "__main__":
    server(ipp)
    time.sleep(2)
    for i in tt:
        i.start()