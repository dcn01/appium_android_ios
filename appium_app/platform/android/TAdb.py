# -*- coding: utf-8 -*-


import os
import random
from time import sleep
import re
import math
from math import ceil
import subprocess


# android 设备连接器
# http://www.cydtest.com/?p=3532
# http://blog.163.com/z_hongc/blog/static/2136400120113176460523/
class TAdb(object):
    # 执行某命令 + 返回执行结果
    def sendCommand(self, command):
        resultText = ''
        command_text = 'adb %s' % command
        # print(command_text)
        results = os.popen(command_text, "r")
        while 1:
            line = results.readline()
            if not line: break
            resultText += line
        results.close()
        return resultText

    # 检查任何快速启动装置
    def fastboot(self, deviceId):
        pass

    # 获取连接的设备
    def getAttachedDevices(self):
        result = self.sendCommand("devices")
        devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
        # flag = [device for device in devices if len(device) > 2]
        # if flag:
        #     return True
        # else:
        #     return False
        return [device for device in devices if len(device) > 2]

    # 连接设备
    def connectDevice(self, ip, port):
        result = self.sendCommand("tcpip " + port)
        result += self.sendCommand("connect " + ip + ":" + port)
        return result

    # 获取设备的状态
    # 设备的状态有3种，device, offline, unknown
    # device：设备正常连接
    # offline：连接出现异常，设备无响应
    # unknown：没有连接设备
    def getState(self):
        result = self.sendCommand("get-state")
        result = result.strip(' \t\n\r')
        return result or None

    # 重启
    def reboot(self, option=''):
        command = "reboot"
        if len(option) > 7 and option in ("bootloader", "recovery",):
            command = "%s %s" % (command, option.strip())
        return self.sendCommand("shell reboot -p")

    # 将电脑文件拷贝到手机里面
    def push(self, local, remote):
        result = self.sendCommand("push %s %s" % (local, remote))
        return result

    # 拉数据到本地
    def pull(self, remote, local):
        result = self.sendCommand("pull %s %s" % (remote, local))
        return result

    # 同步更新
    def sync(self, directory, **kwargs):
        command = "sync %s" % directory
        if 'list' in kwargs:
            command += " -l"
            result = self.sendCommand(command)
            return result

    # 打开指定app
    # adb shell am start -n 包名/包名＋类名（-n 类名,-a action,-d date,-m MIME-TYPE,-c category,-e 扩展数据,等
    def openApp(self, packagename, activity):
        result = self.sendCommand("shell am start -n %s/%s" % (packagename, activity))
        check = result.partition('\n')[2].replace('\n', '').split('\t ')
        if check[0].find("Error") >= 1:
            return False
        return True

    # 根据包名得到进程id
    def getAppPid(self, packagename):
        string = self.sendCommand("shell ps | grep " + packagename)
        # print(string)
        if string == '':
            return "the process doesn't exist."
        result = string.split(" ")
        # print(result[4])
        return result[4]

        # 安装apk  option( -r ) 加 -r 参数，保留已设定数据，重新安装

    def isSoftinputShown(self):
        result = self.sendCommand("shell dumpsys input_method \"| grep mInputShown\" ")
        if result.find("mInputShown=true") >= 1:
            return True;
        result = self.sendCommand("shell dumpsys input_method \"| grep mWindowVisible\" ")  # |grep mWindowVisible"
        if result.find("mWindowVisible=true") >= 1:
            return True;
        return False;

    def installApk(self, filePath, option=""):
        result = "";
        if (len(option) > 0 == True):
            result = self.sendCommand("install " + option + " " + filePath)
        else:
            result = self.sendCommand("install " + filePath)
        result = result.split(" ")
        return result

    # 卸载APK(如果加 -k 参数，为卸载软件但是保留配置和缓存文件)
    # 包的主包名
    def uninstallApk(self, packagename, option=""):
        # adb  apk包的主包名
        # adb install - r apk包
        return self.sendCommand("uninstall " + packagename)

    #获取log日志
    def getLog(self):
        return self.sendCommand("logcat")

    # 获取管理员权限
    def root(self):
        return self.sendCommand("root")

    # 获取设备ID号
    # adb get-serialno
    # 获取设备的ID和序列号：
    #      adb get-product
    #      adb get-serialno

    # 开启adb服务
    def startServer(self):
        return self.sendCommand("start-server")

    # 关闭adb服务
    def killServer(self):
        return self.sendCommand("kill-server")

    # 挂在分区(可使系统分区重新可写)
    def remount(self):
        return self.sendCommand("remount")

    # 发布端口（可以设置任意的端口号，做为主机向模拟器或设备的请求端口）
    # adb forward tcp:5555 tcp:8000

    # 查看bug报告：
    def getBugReport(self):
        return self.sendCommand("bugreport ")

    # 得到手机信息
    def getPhoneInfo(self, devices):
        cmd = "adb -s " + devices + " shell cat /system/build.prop "
        print(cmd)
        # phone_info = os.popen(cmd).readlines()
        phone_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).stdout.readlines()
        result = {"system-realease": "", "model": "", "brand": "", "device": ""}
        release = "ro.build.version.release="  # 版本
        model = "ro.product.model="  # 型号
        brand = "ro.product.brand="  # 品牌
        device = "ro.product.device="  # 设备名
        for line in phone_info:
            for i in line.split():
                temp = i.decode()
                if temp.find(release) >= 0:
                    result["system-realease"] = temp[len(release):]
                    break
                if temp.find(model) >= 0:
                    result["model"] = temp[len(model):]
                    break
                if temp.find(brand) >= 0:
                    result["brand"] = temp[len(brand):]
                    break
                if temp.find(device) >= 0:
                    result["device"] = temp[len(device):]
                    break
        # print(result)
        return result

    # 得到最大运行内存
    def getPhoneMenTotal(self, devices):
        cmd = "adb -s " + devices + " shell cat /proc/meminfo"
        get_cmd = os.popen(cmd).readlines()
        men_total = 0
        men_total_str = "MemTotal"
        for line in get_cmd:
            if line.find(men_total_str) >= 0:
                men_total = line[len(men_total_str) + 1:].replace("kB", "").strip()
                break
        return int(men_total)

    # 得到几核cpu
    def getPhoneCpuKel(self, devices):
        cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
        get_cmd = os.popen(cmd).readlines()
        find_str = "processor"
        int_cpu = 0
        for line in get_cmd:
            if line.find(find_str) >= 0:
                int_cpu += 1
        return str(int_cpu) + "核"

    # 得到手机分辨率
    def getAppPix(self, devices):
        result = os.popen("adb -s " + devices + " shell wm size", "r")
        return result.readline().split("Physical size:")[1]

    def tap(self, x,y):
        os.system("adb shell input tap " + x + " " + y)




if __name__ == '__main__':
    reuslt = TAdb().getAttachedDevices()
    print(reuslt)
    # sleep(1)
    # reuslt = TAdb().connectDevice("10.0.2.15","5555")
    # print(reuslt)
    # sleep(1)
    # reuslt = TAdb().getState()
    # print(reuslt)
    # sleep(1)
    # reuslt = TAdb().getAppPid("com.uc56.ucexpressbao")
    # print(reuslt)
    # sleep(1)
    # reuslt = TAdb().openApp("com.uc56.ucexpressbao", ".activitys.SplashActivity")
    # print(reuslt)
    # sleep(1)
    # reuslt = TAdb().reboot()
    # print(reuslt)
    # sleep(1)
    # print(TAdb().sendCommand("devices"))
    # sleep(1)

    for item in reuslt:
        print(TAdb().getPhoneInfo(item))
        print(TAdb().getPhoneMenTotal(item))
        print(TAdb().getPhoneCpuKel(item))
