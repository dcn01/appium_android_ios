# -*- coding: utf-8 -*-
import unittest
import os
import time
from multiprocessing import Pool

#每个测试用例
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    devices = None

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        global devices
        devices = param

    @classmethod
    def setUpClass(self):
        pass
        # cls.driver = appium_testcase(devices)
        # cls.devicesName = devices["deviceName"]
        # cls.logTest = myLog().getLog(cls.devicesName)  # 每个设备实例化一个日志记录器

    def setUp(self):
        pass
        # self.driver = appium_testcase(self.devices)
        # self.logTest = myLog().getLog(self.devices["deviceName"]) # 每个设备实例化一个日志记录器

    @classmethod
    def tearDownClass(self):
        pass
        # cls.driver.quit()

    def tearDown(self):
        # self.driver.quit()
        pass

    @staticmethod
    def parametrize(testcase_klass, param=None):
        # print("---parametrize-----")
        # print(param)
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite

# class HomeTest(ParametrizedTestCase):
#     # # 清除缓存
#     def testA1ClearCache(self):
#         print("testA1ClearCache");
#
#     # # 无浏览历史页面检测
#     def testA2NoHistory(self):
#         print("testA2NoHistory");
#
# class HomeTest2(ParametrizedTestCase):
#     # # 清除缓存
#     def testA1ClearCache(self):
#         print("testA1ClearCache2");
#
#     # # 无浏览历史页面检测
#     def testA2NoHistory(self):
#         print("testA2NoHistory2");
#
# def runnerCaseApp(devices):
#     starttime = time.now()
#     suite = unittest.TestSuite()
#
#     suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=devices))
#     suite.addTest(ParametrizedTestCase.parametrize(HomeTest2, param=devices))
#     unittest.TextTestRunner(verbosity=2).run(suite)
#     endtime = time.now()
#
# def runnerPool(getDevices):
#     devices_Pool = []
#     for i in range(0, len(getDevices)):
#         print(getDevices[i])
#         devices_Pool.append('test'+getDevices[i])
#
#     pool = Pool(len(devices_Pool))
#     pool.map(runnerCaseApp, devices_Pool)
#     pool.close()
#     pool.join()

if __name__ == '__main__':
    devicess = ['1111111']
    # devicess = ['1111111','22222222222','3333333333']
    # runnerPool(devicess)
    print(devicess)
