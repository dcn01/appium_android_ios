# -*- coding:utf-8 -*-
import yaml as Yaml
from common.TFile import *
import codecs

class TYaml:
    def getYam(self, file):
        if TFile(file, "r").existFile() == False:
            raise Exception('file not exists')
        f = codecs.open(file, 'r+', encoding='utf-8')
        x = Yaml.load(f)
        return x

# if __name__ == '__main__':
#     yaml = TYaml()
#     t = yaml.getYam(r"D:\Project\Python_Project\TestFramework\file\test.yaml")
#     print(t)