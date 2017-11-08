# -*- coding:utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import configparser
import TFile

#邮箱
def read_email(Email):
    if TFile(Email.file, "r").check_file() == False:
        print("文件不存在")
        return
    config = configparser.ConfigParser()
    config.read(Email.file, encoding='utf-8')
    Email.report = "report.xlsx"
    Email.to_addr = eval(config['DEFAULT']['to_addr'])
    Email.mail_host = config['DEFAULT']['mail_host']
    Email.mail_user = config['DEFAULT']['mail_user']
    Email.mail_pass =  config['DEFAULT']['mail_pass']
    Email.port = config['DEFAULT']['port']
    Email.headerMsg = config['DEFAULT']['headerMsg']
    Email.attach = config['DEFAULT']['attach']
    return Email

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(Email):
    '''

    :param f: 附件路径
    :param to_addr:发给的人 []
    :return:
    '''
    from_addr = Email.mail_user
    password = Email.mail_pass
    # to_addr = "ashikun@126.com"
    smtp_server =Email.mail_host

    msg = MIMEMultipart()

    # msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr('lose <%s>' % from_addr)
    msg['To'] = _format_addr('大人 <%s>' % Email.to_addr)
    msg['Subject'] = Header(Email.headerMsg, 'utf-8').encode()

    msg.attach(MIMEText(Email.attach, 'plain', 'utf-8'))
    part = MIMEApplication(open(Email.report, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=Email.report)
    msg.attach(part)

    server = smtplib.SMTP_SSL(smtp_server, Email.port)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, Email.to_addr, msg.as_string())
    server.quit()
