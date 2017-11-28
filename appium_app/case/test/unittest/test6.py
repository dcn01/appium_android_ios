# -*- coding: utf-8 -*-
import unittest

class TestCase1(unittest.TestCase):
    # def setUp(self):
    # def tearDown(self):
    def testCase1(self):
        print('aaa')

    def testCase2(self):
        print('bbb')

class TestCase2(unittest.TestCase):
    # def setUp(self):
    # def tearDown(self):
    def testCase1(self):
        print('aaa1')

    def testCase2(self):
        print('bbb1')

def test():
    # 此用法可以同时测试多个类
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestCase1)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestCase2)
    suite = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test();