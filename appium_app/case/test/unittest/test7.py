# -*- coding: utf-8 -*-
import appium_app.case.test.unittest.test6 as test6
import appium_app.case.test.unittest.test5 as test5
import appium_app.case.test.unittest.test4 as test4

class TestCase1():
    # def setUp(self):
    # def tearDown(self):
    def testCase1(self):
        print('aaa')

    def testCase2(self):
        print('bbb')

if __name__ == "__main__":
    # 此用法可以同时测试多个类
    print("")
    # test6.test();
    # test5.test();
    test4.test();