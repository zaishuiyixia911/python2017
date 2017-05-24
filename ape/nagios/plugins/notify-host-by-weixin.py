#!/usr/bin/python
#_*_ coding:utf-8 _*_

import urllib.request
import json
import sys

def gettoken(corp_id,corp_secret):
	gettoken_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+corp_id+'&secret='+corp_secret
	try:
		token_file = urllib.request.urlopen(gettoken_url)
	except urllib.error.HTTPError as e:
		print (e.code)
		print (e.read().decode("utf-8"))
	token_data = token_file.read().decode('utf-8')
	token_json = json.loads(token_data)
	token_json.keys()
	token = token_json['access_token']
	return token

def senddata(access_token,notify_str):
	send_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='+access_token
	notifydata = notify_str.split("separator")
	user = notifydata[0]
	cationtype = notifydata[1]
	name = notifydata[2]
	state = notifydata[3]
	address = notifydata[4]
	output = notifydata[5]
	datatime = notifydata[6]
	content = 'Nagios 警报  \n\n 类型 : ' + cationtype + '\n 主机名 : ' + name + '\n 状态 : ' + state + '\n IP 地址 : ' + address + '\n 日志 : ' + output + '\n\n 时间 : ' + datatime + '\n'
	send_values = {
		      "touser":user,
		      "msgtype":"text",
		      "agentid":"0",
		      "text":{
		      "content":content
		      },
		      "safe":"0"
		      }
	send_data = json.dumps(send_values, ensure_ascii=False).encode(encoding='UTF8')
	send_request = urllib.request.Request(send_url, send_data)
	response = urllib.request.urlopen(send_request)
	msg = response.read()
	return msg
if __name__ == '__main__':
#	default_encoding = 'utf-8'
#	if sys.getdefaultencoding() != default_encoding:
#		reload(sys)
#	sys.setdefaultencoding(default_encoding)
#	reload(__import__('sys')).setdefaultencoding('utf-8')
	notifystr = str(sys.argv[1])
	corpid = 'yeruiwxdced045fe0c80b59'
	corpsecret = 'liangff638238b96e0862d42fc04b023e4edf'
	accesstoken = gettoken(corpid,corpsecret)
	msg = senddata(accesstoken,notifystr)
	print(msg)


