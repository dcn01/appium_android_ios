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
    def __init__(self, filePath, statisticsName=u"测试总况", detailName=u"测试详情"):
        self.workbook = xlsxwriter.Workbook(filePath)
        self.statisticsWorksheet = None
        self.detailWorksheet = None
        self.initStatisticsHeader(statisticsName)
        self.initDetailHead(detailName)
        self.detailWorksheetLine = 2

    def close(self):
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

    def initStatisticsHeader(self, name):
        self.statisticsWorksheet = self.workbook.add_worksheet(name)

        # 设置列行的宽高（设置一列或多列单元格属性）
        self.statisticsWorksheet.set_column("A:A", 15)
        self.statisticsWorksheet.set_column("B:B", 20)
        self.statisticsWorksheet.set_column("C:C", 20)
        self.statisticsWorksheet.set_column("D:D", 20)
        self.statisticsWorksheet.set_column("E:E", 20)

        self.statisticsWorksheet.set_row(1, 30)  # 高度为30像素
        self.statisticsWorksheet.set_row(2, 30)
        self.statisticsWorksheet.set_row(3, 30)
        self.statisticsWorksheet.set_row(4, 30)
        self.statisticsWorksheet.set_row(5, 30)

        define_format_H1 = addFormat(self.workbook, {'bold': True, 'font_size': 18})
        define_format_H2 = addFormat(self.workbook, {'bold': True, 'font_size': 14})
        define_format_H1.set_border(1)

        define_format_H2.set_border(1)
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H2.set_bg_color("blue")
        define_format_H2.set_color("#ffffff")

        self.statisticsWorksheet.merge_range('A1:E1', '测试报告总概况', define_format_H1)
        self.statisticsWorksheet.merge_range('A2:E2', '测试概括', define_format_H2)

        writeCenter(self.statisticsWorksheet, "A3", 'APP名称', self.workbook)
        writeCenter(self.statisticsWorksheet, "A4", 'APP大小', self.workbook)
        writeCenter(self.statisticsWorksheet, "A5", 'APP版本', self.workbook)
        writeCenter(self.statisticsWorksheet, "A6", '测试日期', self.workbook)

        writeCenter(self.statisticsWorksheet, "C3", "用例总数", self.workbook)
        writeCenter(self.statisticsWorksheet, "C4", "通过总数", self.workbook)
        writeCenter(self.statisticsWorksheet, "C5", "失败总数", self.workbook)
        writeCenter(self.statisticsWorksheet, "C6", "测试耗时", self.workbook)

    def initStatisticsData(self, data):
        writeCenter(self.statisticsWorksheet, "B3", data['appName'], self.workbook)
        writeCenter(self.statisticsWorksheet, "B4", data['appSize'], self.workbook)
        writeCenter(self.statisticsWorksheet, "B5", data['appVersion'], self.workbook)
        writeCenter(self.statisticsWorksheet, "B6", data['testDate'], self.workbook)

        # data1 = {"test_sum": 100, "test_success": 80, "test_failed": 20, "test_date": "2018-10-10 12:10"}
        writeCenter(self.statisticsWorksheet, "D3", data['sum'], self.workbook)
        writeCenter(self.statisticsWorksheet, "D4", data['pass'], self.workbook)
        writeCenter(self.statisticsWorksheet, "D5", data['fail'], self.workbook)
        writeCenter(self.statisticsWorksheet, "D6", data['testSumDate'], self.workbook)

        writeCenter(self.statisticsWorksheet, "E3", "脚本语言", self.workbook)
        self.statisticsWorksheet.merge_range('E4:E6', 'appium+python3', addFormatForCenter(self.workbook))
        pie(self.workbook, self.statisticsWorksheet)

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

    def initDetailHead(self, name):
        self.detailWorksheet = self.workbook.add_worksheet(name)
        # String.encodeUtf8()
        # 设置列行的宽高
        self.detailWorksheet.set_column("A:A", 30)
        self.detailWorksheet.set_column("B:B", 20)
        self.detailWorksheet.set_column("C:C", 20)
        self.detailWorksheet.set_column("D:D", 20)
        self.detailWorksheet.set_column("E:E", 20)
        self.detailWorksheet.set_column("F:F", 20)
        self.detailWorksheet.set_column("G:G", 20)
        self.detailWorksheet.set_column("H:H", 20)
        self.detailWorksheet.set_column("I:I", 20)
        self.detailWorksheet.set_column("J:J", 20)
        self.detailWorksheet.set_column("K:K", 20)

        self.detailWorksheet.set_row(1, 30)
        self.detailWorksheet.set_row(2, 30)
        self.detailWorksheet.set_row(3, 30)
        self.detailWorksheet.set_row(4, 30)
        self.detailWorksheet.set_row(5, 30)
        self.detailWorksheet.set_row(6, 30)
        self.detailWorksheet.set_row(7, 30)
        self.detailWorksheet.set_row(8, 30)
        self.detailWorksheet.set_row(9, 30)
        self.detailWorksheet.set_row(10, 30)
        self.detailWorksheet.set_row(11, 30)

        self.detailWorksheet.merge_range('A1:K1', '测试详情',
                                         addFormat(self.workbook, {'bold': True, 'font_size': 18, 'align': 'center',
                                                                   'valign': 'vcenter', 'bg_color': 'blue',
                                                                   'font_color': '#ffffff'}))
        writeCenter(self.detailWorksheet, "A2", '机型', self.workbook)
        writeCenter(self.detailWorksheet, "B2", '用例ID', self.workbook)
        writeCenter(self.detailWorksheet, "C2", '用例名称', self.workbook)
        writeCenter(self.detailWorksheet, "D2", '用例介绍', self.workbook)
        writeCenter(self.detailWorksheet, "E2", '用例函数', self.workbook)
        writeCenter(self.detailWorksheet, "F2", '前置条件 ', self.workbook)
        writeCenter(self.detailWorksheet, "G2", '操作步骤 ', self.workbook)
        writeCenter(self.detailWorksheet, "H2", '检查点', self.workbook)
        writeCenter(self.detailWorksheet, "I2", '测试结果', self.workbook)
        writeCenter(self.detailWorksheet, "J2", '备注', self.workbook)
        writeCenter(self.detailWorksheet, "K2", '截图', self.workbook)

    def initDetailData(self, data):
        self.detailWorksheetLine += 1  # 行 默认是从第3行开始
        if ("phoneClass" in data):  # 手机类型
            writeCenter(self.detailWorksheet, "A" + str(self.detailWorksheetLine), data["phoneClass"], self.workbook)
        if ("id" in data):  # 案例序列
            writeCenter(self.detailWorksheet, "B" + str(self.detailWorksheetLine), data["id"], self.workbook)
        if ("caseName" in data):  # 案例名称
            writeCenter(self.detailWorksheet, "C" + str(self.detailWorksheetLine), data["caseName"], self.workbook)
        if ("caseDescription" in data):  # 案例介绍
            writeCenter(self.detailWorksheet, "D" + str(self.detailWorksheetLine), data["caseDescription"],
                        self.workbook)
        if ("caseFunction" in data):  # 案例函数
            writeCenter(self.detailWorksheet, "E" + str(self.detailWorksheetLine), data["caseFunction"], self.workbook)
        if ("precondition" in data):  # 前置条件
            writeCenter(self.detailWorksheet, "F" + str(self.detailWorksheetLine), data["precondition"], self.workbook)
        if ("step" in data):  # 操作步骤
            writeCenter(self.detailWorksheet, "G" + str(self.detailWorksheetLine), data["step"], self.workbook)
        if ("checkpoint" in data):  # 检查点
            writeCenter(self.detailWorksheet, "H" + str(self.detailWorksheetLine), data["checkpoint"], self.workbook)
        if ("result" in data):  # 结果（通过，不通过）
            writeCenter(self.detailWorksheet, "I" + str(self.detailWorksheetLine), data["result"], self.workbook)
        if ("remarks" in data):  # 备注
            writeCenter(self.detailWorksheet, "J" + str(self.detailWorksheetLine), data["remarks"], self.workbook)
        if ("screenshot" in data):  # 截图
            try:
                self.detailWorksheet.insert_image('K' + str(self.detailWorksheetLine), data["screenshot"],
                                                  {'x_scale': 0.1, 'y_scale': 0.1, 'border': 1})
                self.detailWorksheet.set_row(self.detailWorksheetLine - 1, 110)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    sum = {'testSumDate': '25秒', 'sum': 20, 'pass': 15, 'testDate': '2017-06-05 15:26:49', 'fail': 5,
           'appVersion': '17051515', 'appSize': '14M', 'appName': "简书"}
    info = [
        {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
         "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
         "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
        {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
         "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
         "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
        {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
         "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
         "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
        {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
         "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
         "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
        {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
         "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
         "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"},
        {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
         "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
         "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"}
    ]

    # info = {"phoneClass": "三星", "id": 1, "caseName": "testf01", "caseDescription": "第一次打开", "caseFunction": "函数",
    #         "precondition": "前置条件", "step": "通过", "checkpoint": "检查点", "result": "通过", "remarks": "哈哈",
    #         "screenshot": "D:\\Project\\Python_Project\\TestFramework\\file\\test.jpg"}

    output_file = (
        "D:\\Project\\Python_Project\\TestFramework\\file\\" + 'report_%s.xlsx' % datetime.datetime.now().strftime(
            '%Y-%m-%d-%H-%M-%S'))
    excel = TExcel(output_file, u"测试总况", u"测试详情")
    excel.initStatisticsData(sum)

    for item in info:
        excel.initDetailData(item)
    del excel
