# -*- coding: utf-8 -*-
import os
import urllib
from multiprocessing import Process
import threading
import time
import random
from appium_app.platform.android.TAdb import *
from appium_app.platform.core.Executor import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# appium 启动服务
class TAppiumServer(Executor):
    def __init__(self):
        pass

    def __init__(self, port, bport, devices):
        self.port = str(port)
        self.bport = str(bport)
        self.devices = devices

    # 启动服务
    def startServer(self):
        print("start server for %s" % self.devices)
        cmd = u"appium --session-override  -p %s -bp %s -U %s" % (self.port, self.bport, self.devices)
        # appium -a 127.0.0.1 -p 4727 -bp 4728 -U 3DN6T16827002332 --session-override
        runServer = RunServer(cmd)
        process = Process(target=runServer.start())
        process.start()

    # 停止服务
    def stopServer(self):
        print("stop server for %s" % self.devices)
        # os.system('taskkill /f /im  node.exe')
        # mac
        cmd = "lsof -i :{0}".format("4725")
        plist = os.popen(cmd).readlines()
        plisttmp = plist[1].split("    ")
        plists = plisttmp[1].split(" ")
        # print plists[0]
        os.popen("kill -9 {0}".format(plists[0]))

    # 重启服务
    def reStartServer(self):
        self.stopServer()
        self.startServer()

    # 是否在运行
    def isRunnnig(self):
        response = None
        url = " http://127.0.0.1:" + self.port + "/wd/hub" + "/status"
        try:
            response = urllib.request.urlopen(url, timeout=5)
            if str(response.getcode()).startswith("2"):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            if response:
                response.close()

    def event(self, element, eventType="click", params=None, yamlParam=None):
        super().event(element, eventType, params, yamlParam)

    def find(self, findField, findType='xpath', index=0):
        super().event(findField, findType, index)


class RunServer(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)


# 目前失效
if __name__ == "__main__":
    devicess = TAdb().getAttachedDevices()
    if len(devicess) > 0:
        l_devices = []
        for devices in devicess:
            app = {}
            port = 4723  # random.randint(4700, 4900)
            bpport = 4775  # random.randint(4700, 4900)
            app["port"] = str(port)
            app["devices"] = devices
            l_devices.append(app)
            appium_server = TAppiumServer(port=port, bport=bpport, devices=devices)
            appium_server.startServer()
            while not appium_server.isRunnnig():
                time.sleep(2)
            print("test")
            # runnerPool(l_devices)
            # stopAppiumMacAndroid(l_devices)
            # writeExcel()
    else:
        print("没有可用的安卓设备")
