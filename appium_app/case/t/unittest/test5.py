# -*- coding: utf-8 -*-
import urllib
import unittest

import random

class TestTTT:
    def tet(self):
        print("test")

class TestSequenceFunctions(unittest.TestCase):

   def setUp(self):
       self.seq = range(10)

   def tearDown(self):
       super().tearDown()

   @classmethod
   def setUpClass(cls):
       super().setUpClass()

   @classmethod
   def tearDownClass(cls):
       super().tearDownClass()

   def test_shuffle(self):
       print("")
       # make sure the shuffled sequence does not lose any elements
       # random.shuffle(self.seq)
       # self.seq.sort()
       # self.assertEqual(self.seq, range(10))
       # should raise an exception for an immutable sequence
       # self.assertRaises(TypeError, random.shuffle, (1,2,3))

   def test_choice(self):
       element = random.choice(self.seq)
       self.assertTrue(element in self.seq)

   def test_error(self):
       print("test_error")
          # element = random.choice(self.seq)
          # self.assertTrue(element not in self.seq)

def test():
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(TestSequenceFunctions("test_shuffle"))
    suite.addTest(TestSequenceFunctions("test_choice"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    print("")
    test()