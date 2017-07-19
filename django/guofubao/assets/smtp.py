#!/usr/bin/python
#_*_ coding:utf-8 _*_

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr, formatdate
import smtplib

def _format_addr(s):
	name,addr = parseaddr(s)
	return formataddr((Header(name,'utf-8').encode(),addr))
def sendmail():
    from_addr = "111@163.com"
    password = "aaa"
    to_addr = "222@163.com"
    smtp_server = "smtp.163.com"
    
    # 邮件对象:
    msg = MIMEMultipart('alternative')
    msg['From'] = _format_addr('快讯 <%s>' % from_addr)
    msg['To'] = _format_addr('老王 <%s>' % to_addr)
    msg['Subject'] = Header('快讯', 'utf-8').encode()
    msg.attach(MIMEText('举行合作交流座谈会', 'plain', 'utf-8'))
    #msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))
    
    
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

if __name__ == '__main__':
    sendmail()
