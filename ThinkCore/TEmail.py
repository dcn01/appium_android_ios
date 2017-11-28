# -*- coding:utf-8 -*-

import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import configparser

from ThinkCore.TFile import *
import ThinkCore.TString as String

def hasConfigKey(config,name,key):
    try:
        config[name][key]
        return True
    except Exception as e:
        print(e)
    return False

def getConfigValue(config,name,key):
    try:
        return config[name][key]
    except Exception as e:
        print(e)
    return ""

# 邮箱
class TEmail:
    def __init__(self):
        pass

    def __init__(self, file):
        if TFile(file, "r").existFile() == False:
            raise Exception('file not exists')
        # 读取配置信息
        config = configparser.ConfigParser()
        config.read(file, encoding='utf-8')
        if(hasConfigKey(config,'DEFAULT','to_addr')):
            self.to_addr = eval(getConfigValue(config,'DEFAULT','to_addr'))
        if (hasConfigKey(config, 'DEFAULT', 'mail_host')):
            self.mail_host = getConfigValue(config,'DEFAULT','mail_host')
        if (hasConfigKey(config, 'DEFAULT', 'mail_user')):
            self.mail_user = config['DEFAULT']['mail_user']
        if (hasConfigKey(config, 'DEFAULT', 'mail_pass')):
            self.mail_pass = config['DEFAULT']['mail_pass']
        if (hasConfigKey(config, 'DEFAULT', 'port')):
            self.port = config['DEFAULT']['port']
        if (hasConfigKey(config, 'DEFAULT', 'title')):
            self.title = config['DEFAULT']['title']
        if (hasConfigKey(config, 'DEFAULT', 'body')):
            self.body = config['DEFAULT']['body']

    def formatAddr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

        '''
        :param f: 附件路径
        :param to_addr:发给的人 []
        :return:
        '''

    def sendMail(self, reportFile):
        if (len(self.mail_user) < 0 | len(self.mail_pass) < 0 | len(self.to_addr) < 0 | len(self.mail_host) < 0 | len(
                self.title) < 0 | len(self.body) < 0 | len(self.port) < 0 ):
            raise Exception("send email params empty!~~~")

        from_addr = self.mail_user #来源
        password = self.mail_pass #来源密码
        to_addr = self.to_addr #发给谁["",""]
        smtp_server = self.mail_host #邮箱服务平台
        title = self.title #名称
        body = self.body #内容
        port = self.port #端口

        msg = MIMEMultipart()
        # msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
        msg['From'] = self.formatAddr('案例执行 <%s>' % from_addr)
        msg['To'] = self.formatAddr('各位领导和同事 <%s>' % to_addr)
        msg['Subject'] = Header(title, 'utf-8').encode()
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        if TFile(reportFile, "r").existFile() == True:
            part = MIMEApplication(open(reportFile, 'rb').read())  # 附件
            part.add_header('Content-Disposition', 'attachment', filename=TFile(reportFile).getFileName())
            msg.attach(part)
        try:
            smtpServer = smtplib.SMTP()
            smtpServer.connect(smtp_server, int(port))  # 25 为 SMTP 端口号
            # smtpServer.set_debuglevel(1)
            smtpServer.login(from_addr, password)
            smtpServer.sendmail(from_addr, to_addr, msg.as_string())
            print("email send success")
        except smtplib.SMTPException as e:
            print("Error: %s" % e)
        finally:
            smtpServer.quit()


if __name__ == '__main__':
    email = TEmail(r"D:\Project\Python_Project\TestFramework\file\email.ini")
    email.sendMail(r"D:\Project\Python_Project\TestFramework\file\11111.txt")


    # def test(self):
    #     # 第三方 SMTP 服务
    #     mail_host = "smtp.126.com"  # 设置服务器
    #     mail_user = "fuzhouxiu@126.com"  # 用户名
    #     mail_pass = "0416456aaa"  # 口令
    #
    #     sender = 'fuzhouxiu@126.com'
    #     receivers = ['411488747@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #
    #     message = MIMEText('MyGod', 'plain')
    #     message['From'] = Header(sender, 'utf-8').encode()
    #     message['To'] = Header('411488747@qq.com', 'utf-8').encode()
    #     message['Subject'] = Header("MyGod", 'utf-8').encode()
    #     mail = [
    #         "From: %s <%s>" % ("公司", sender),
    #         "To: %s" % ','.join(receivers),  # 转成字符串，以逗号分隔元素
    #         "Subject: %s" % "MyGod",
    #         "Cc: %s" % ','.join(['banketree@qq.com']),
    #         "", "12345678910"
    #     ]
    #     msg = '\n'.join(mail)
    #     try:
    #         smtpObj = smtplib.SMTP()
    #         smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    #         smtpObj.login(mail_user, mail_pass)
    #         smtpObj.sendmail(sender, '411488747@qq.com', msg)
    #         print "邮件发送成功"
    #     except smtplib.SMTPException as e:
    #         print "Error: %s" % e