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
def sendmail(send):
    from_addr = "111@163.com"
    password = "aaa"
    to_addr = "222@163.com"
    smtp_server = "smtp.163.com"
    
    print "***********************"
    print ("send",send)
    # 邮件对象:
    msg = MIMEMultipart('alternative')
    msg['From'] = _format_addr('运维中心 <%s>' % from_addr)
    msg['To'] = _format_addr(' <%s>' % to_addr)
    msg['Subject'] = Header('运维中心工单审核通知', 'utf-8').encode()
    #msg.attach(MIMEText('中国电信海南分公司与海航通信在数据谷举行合作交流座谈会', 'plain', 'utf-8'))
    msg.attach(MIMEText(send, 'plain', 'utf-8'))
    msg.attach(MIMEText('<html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body><div>各位领导、同事：</div><div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;提交的工单已经通过审核，请相关人员按照工单执行，详细如下。</div><div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+send+'</div><div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;有问题请点击并登录<a href="http://192.168.1.33:8000">运维中心</a>查询。</div></body></html>', 'html', 'utf-8'))
    
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

if __name__ == '__main__':
    sendmail(send)
