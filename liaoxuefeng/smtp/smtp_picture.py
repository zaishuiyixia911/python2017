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

from_addr = "123@163.com"
password = "123456"
to_addr = "456@hnair.com"
smtp_server = "smtp.163.com"

# 邮件对象:
msg = MIMEMultipart('alternative')
msg['From'] = _format_addr('海航生态科技快讯 <%s>' % from_addr)
msg['To'] = _format_addr('老王 <%s>' % to_addr)
msg['Subject'] = Header('海航生态科技快讯', 'utf-8').encode()
msg.attach(MIMEText('<html><body><h1 style="font-size:15px">中国电信海南分公司与海航通信在数据谷举行合作交流座谈会</h1>' +
    '<p><img src="cid:0"></p>' +
    '<h1 style="font-size:13px">2017年2月14日下午，中国电信海南分公司市场部总经理陈莹、宽带运营部总经理龙飞和政企客户部行业总监符强等一行调研海南数据谷，参观了数据谷办公空间。随后举行座谈会，海南电信愿意进一步加深双方在海南地区的合作，为海航通信提供充足的本地码号资源及出口带宽资源，更在未来结合海航集团的丰富地区资源，共同开发全省宽带、专线业务和Wi-Fi运营，助力加速全岛宽带建设，双方将发展为长期战略合作伙伴，实现双方的共享共赢。海航通信总经理殷建、副总经理丁利平陪同出席上述活动。</h1>' +
    '</body></html>', 'html', 'utf-8'))
#msg.attach(MIMEText('中国电信海南分公司与海航通信在数据谷举行合作交流座谈会', 'plain', 'utf-8'))
#msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))

with open('/home/shao/smtp/ddd.png', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='ddd.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='ddd.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)

server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
