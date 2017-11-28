# -*- coding:utf-8 -*-
import yaml as Yaml
from ThinkCore.TFile import *
import codecs

class TYaml:
    def getYam(self, file):
        try:
            if TFile(file, "r").existFile() == False:
                return None
            f = codecs.open(file, 'r+', encoding='utf-8')
            x = Yaml.load(f)
            return x
        except Exception as e:
            print(e)
        return None

# if __name__ == '__main__':
    # yaml = TYaml()
    # t = yaml.getYam(r"D:\Project\Python_Project\TestFramework\file\test.yaml")
    # print(t["testinfo"][0])
    # print(t["testcase"][1])
    # print(t["testcase"][1]['element_info'])
    # print(t["testcase"][0])
    # print(t["check"])
    # print(t)