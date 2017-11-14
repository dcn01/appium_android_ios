# -*- coding: utf-8 -*-
import os
import urllib
from multiprocessing import Process
import threading
import time
import random
from TAdb import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

#appium 启动服务
class TAppium:

    def __init__(self, port, bport, devices):
        self.port = str(port)
        self.bport = str(bport)
        self.devices = devices

    #启动服务
    def startServer(self):
        print("start server for %s" % self.devices)
        cmd = "appium --session-override  -p %s -bp %s -U %s" %(self.port, self.bport, self.devices)
        runServer = RunServer(cmd)
        process = Process(target=runServer.start())
        process.start()

    #停止服务
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

    #重启服务
    def reStartServer(self):
        self.stopServer()
        self.startServer()

    #是否在运行
    def isRunnnig(self):
        response = None
        url = " http://127.0.0.1:"+ self.port + "/wd/hub"+"/status"
        try:
            response = urllib.urlopen(url, timeout=5)
            if str(response.getcode()).startswith("2"):
                return True
            else:
                return False
        except Exception as e:
            print e
            return False
        finally:
            if response:
                response.close()

class RunServer(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
    def run(self):
        os.system(self.cmd)

#目前失效
if __name__ == "__main__":
    devicess = TAdb().getAttachedDevices()
    if len(devicess) > 0:
        l_devices = []
        for devices in devicess:
            app = {}
            port = 4723#random.randint(4700, 4900)
            bpport = 4775#random.randint(4700, 4900)
            app["port"] = str(port)
            app["devices"] = devices
            l_devices.append(app)
            appium_server = TAppium(port=port, bport=bpport, devices=devices)
            appium_server.startServer()
            while not appium_server.isRunnnig():
                time.sleep(2)
            print "test"
        # runnerPool(l_devices)
        # stopAppiumMacAndroid(l_devices)
        # writeExcel()
    else:
        print("没有可用的安卓设备")