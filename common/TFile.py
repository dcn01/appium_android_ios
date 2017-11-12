# -*- coding:utf-8 -*-
import os

'''
操作文件
'''

class TFile:
    # method(r,w,a)
    def __init__(self, file, method='w+'):
        self.file = file
        self.method = method
        self.fileHandle = None

    def writeTxt(self, line):
        if self.existFile():
            self.fileHandle = open(self.file, self.method)
            self.fileHandle.write(line + "\n")
            self.fileHandle.close()

    def appendTxt(self, line):
        if self.existFile():
            self.fileHandle = open(self.file, 'a')
            self.fileHandle.write(line + "\n")
            self.fileHandle.close()

    def readTxtRow(self):
        resutl = ""
        if self.existFile():
            self.fileHandle = open(self.file, self.method)
            resutl = self.fileHandle.readline()
            self.fileHandle.close()
        return resutl

    def readTxtRows(self):
        if self.existFile():
            self.fileHandle = open(self.file, self.method)
            file_list = self.fileHandle.readlines()
            for i in file_list:
                print(i.strip("\n"))
            self.fileHandle.close()

    def existFile(self):
        if not os.path.exists(self.file):#文件不存在
            return False
        #文件存在
        return True

    def mkFile(self):
        if self.existFile():
            f = open(self.file, self.method)
            f.close()
            # print("创建文件成功")
            pass
        else:
            print("文件已经存在")

    def removeFile(self):
        if self.existFile():#删除文件成功
            os.remove(self.file)
            print("")
        else:#文件不存在
            pass

    def getFileName(self):
        if self.existFile()==False:  # 文件不存在
            return False
        return os.path.basename(self.file)

# if __name__ == '__main__':
#     bf = TFile(r"D:\Project\Python_Project\TestFramework\file\11111.txt")
#     print(bf.getFileName())
#     if bf.existFile() == False:
#         bf.mkFile()
#     bf.writeTxt("2222222222222")
#     bf.appendTxt("33333333333333333")
#     bf.appendTxt("344444444444444444")
