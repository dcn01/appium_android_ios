# -*- coding:utf-8 -*-

import xlsxwriter
import os
import datetime

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# def link_format(wd):
#     red_format = wd.add_format({
#         'font_color': 'red',
#         'bold': 1,
#         'underline': 1,
#         'font_size': 12,
#     })

# 添加一种格式
def addFormat(workbook, option={}):
    return workbook.add_format(option)

# 添加一种居中格式
def addFormatForCenter(workbook, border=1):
    return addFormat(workbook, {'align': 'center', 'valign': 'vcenter', 'border': border});

# 添加边框
def addBorder(worksheet, border=1):
    return addFormat(worksheet).set_border(border)

# 写入
def writeCenter(worksheet, column, data, workbook):
    return worksheet.write(column, data, addFormatForCenter(workbook))

# 赋值高
def setRowHeight(worksheet, row, height):
    worksheet.set_row(row, height)

# 生成饼形图
def pie(workbook, worksheet):
    chart1 = workbook.add_chart({'type': 'pie'})
    chart1.add_series({
        'name': '自动化测试统计',
        'categories': '=测试总况!$C$4:$C$5',
        'values': '=测试总况!$D$4:$D$5',
    })
    chart1.set_title({'name': '测试统计'})
    chart1.set_style(10)
    worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})


# 生成测试报表
class TExcel:
    def __init__(self, filePath):
        self.workbook = xlsxwriter.Workbook(filePath)

    def __del__(self):
        self.workbook.close();

    def getWorkbook(self):
        return self.workbook;

    '''｛
   appName：APP名称
   appSize：APP大小
   appVersion：版本号
   testDate：测试日期
   sum：用例总数
   pass：通过总数
   fail：失败总数
   testSumDate：测试耗时
   ｝'''

    def statistics(self, name, data):
        worksheet = self.workbook.add_worksheet(name)

        # 设置列行的宽高（设置一列或多列单元格属性）
        worksheet.set_column("A:A", 15)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)

        worksheet.set_row(1, 30)  # 高度为30像素
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)

        define_format_H1 = addFormat(self.workbook, {'bold': True, 'font_size': 18})
        define_format_H2 = addFormat(self.workbook, {'bold': True, 'font_size': 14})
        define_format_H1.set_border(1)

        define_format_H2.set_border(1)
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H2.set_bg_color("blue")
        define_format_H2.set_color("#ffffff")

        worksheet.merge_range('A1:E1', '测试报告总概况', define_format_H1)
        worksheet.merge_range('A2:E2', '测试概括', define_format_H2)

        writeCenter(worksheet, "A3", 'APP名称', self.workbook)
        writeCenter(worksheet, "A4", 'APP大小', self.workbook)
        writeCenter(worksheet, "A5", 'APP版本', self.workbook)
        writeCenter(worksheet, "A6", '测试日期', self.workbook)

        writeCenter(worksheet, "B3", data['appName'], self.workbook)
        writeCenter(worksheet, "B4", data['appSize'], self.workbook)
        writeCenter(worksheet, "B5", data['appVersion'], self.workbook)
        writeCenter(worksheet, "B6", data['testDate'], self.workbook)

        writeCenter(worksheet, "C3", "用例总数", self.workbook)
        writeCenter(worksheet, "C4", "通过总数", self.workbook)
        writeCenter(worksheet, "C5", "失败总数", self.workbook)
        writeCenter(worksheet, "C6", "测试耗时", self.workbook)

        # data1 = {"test_sum": 100, "test_success": 80, "test_failed": 20, "test_date": "2018-10-10 12:10"}
        writeCenter(worksheet, "D3", data['sum'], self.workbook)
        writeCenter(worksheet, "D4", data['pass'], self.workbook)
        writeCenter(worksheet, "D5", data['fail'], self.workbook)
        writeCenter(worksheet, "D6", data['testSumDate'], self.workbook)

        writeCenter(worksheet, "E3", "脚本语言", self.workbook)
        worksheet.merge_range('E4:E6', 'appium+python3', addFormatForCenter(self.workbook))
        pie(self.workbook, worksheet)

    '''
   phoneClass：手机类型     
   id：案例序列
   caseName：案例名称
   caseDescription：案例介绍
   caseFunction：案例函数
   precondition：前置条件
   step：操作步骤
   checkpoint：检查点 
   result：结果（通过，不通过）
   remarks：备注
   screenshot：截图
   '''

    def detail(self, name, data):
        worksheet = self.workbook.add_worksheet(name)
        # String.encodeUtf8()
        # 设置列行的宽高
        worksheet.set_column("A:A", 30)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)
        worksheet.set_column("G:G", 20)
        worksheet.set_column("H:H", 20)
        worksheet.set_column("I:I", 20)
        worksheet.set_column("J:J", 20)
        worksheet.set_column("K:K", 20)

        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)
        worksheet.set_row(8, 30)
        worksheet.set_row(9, 30)
        worksheet.set_row(10, 30)
        worksheet.set_row(11, 30)

        worksheet.merge_range('A1:K1', '测试详情',
                              addFormat(self.workbook, {'bold': True, 'font_size': 18, 'align': 'center',
                                                        'valign': 'vcenter', 'bg_color': 'blue',
                                                        'font_color': '#ffffff'}))
        writeCenter(worksheet, "A2", '机型', self.workbook)
        writeCenter(worksheet, "B2", '用例ID', self.workbook)
        writeCenter(worksheet, "C2", '用例名称', self.workbook)
        writeCenter(worksheet, "D2", '用例介绍', self.workbook)
        writeCenter(worksheet, "E2", '用例函数', self.workbook)
        writeCenter(worksheet, "F2", '前置条件 ', self.workbook)
        writeCenter(worksheet, "G2", '操作步骤 ', self.workbook)
        writeCenter(worksheet, "H2", '检查点', self.workbook)
        writeCenter(worksheet, "I2", '测试结果', self.workbook)
        writeCenter(worksheet, "J2", '备注', self.workbook)
        writeCenter(worksheet, "K2", '截图', self.workbook)

        line = 3  # 第三行开始
        for item in data:
            # print(item)
            if ("phoneClass" in item):  # 手机类型
                writeCenter(worksheet, "A" + str(line), item["phoneClass"], self.workbook)
            if ("id" in item):  # 案例序列
                writeCenter(worksheet, "B" + str(line), item["id"], self.workbook)
            if ("caseName" in item):  # 案例名称
                writeCenter(worksheet, "C" + str(line), item["caseName"], self.workbook)
            if ("caseDescription" in item):  # 案例介绍
                writeCenter(worksheet, "D" + str(line), item["caseDescription"], self.workbook)
            if ("caseFunction" in item):  # 案例函数
                writeCenter(worksheet, "E" + str(line), item["caseFunction"], self.workbook)
            if ("precondition" in item):  # 前置条件
                writeCenter(worksheet, "F" + str(line), item["precondition"], self.workbook)
            if ("step" in item):  # 操作步骤
                writeCenter(worksheet, "G" + str(line), item["step"], self.workbook)
            if ("checkpoint" in item):  # 检查点
                writeCenter(worksheet, "H" + str(line), item["checkpoint"], self.workbook)
            if ("result" in item):  # 结果（通过，不通过）
                writeCenter(worksheet, "I" + str(line), item["result"], self.workbook)
            if ("remarks" in item):  # 备注
                writeCenter(worksheet, "J" + str(line), item["remarks"], self.workbook)
            if ("screenshot" in item):  # 截图
                try:
                    worksheet.insert_image('K' + str(line), item["screenshot"],
                                           {'x_scale': 0.1, 'y_scale': 0.1, 'border': 1})
                    worksheet.set_row(line - 1, 110)
                except Exception as e:
                    print(e)
            line = line + 1

# if __name__ == '__main__':
#     sum = {'testSumDate': '25秒', 'sum': 20, 'pass': 15, 'testDate': '2017-06-05 15:26:49', 'fail': 5,
#            'appVersion': '17051515', 'appSize': '14M', 'appName': "简书"}
#     info = [
#         {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
#          "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
#          "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
#         {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
#          "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
#          "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
#         {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
#          "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
#          "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
#         {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
#          "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
#          "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
#         {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
#          "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
#          "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
#         {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
#          "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
#          "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"}
#     ]
#
#     output_file = (
#         "D:\\Project\\Python_Project\\TestFramework\\file\\" + 'report_%s.xlsx' % datetime.datetime.now().strftime(
#             '%Y-%m-%d-%H-%M-%S'))
#     excel = TExcel(output_file)
#     excel.statistics(u"测试总况", sum)
#     excel.detail(u"测试详情", info)
#     del excel
