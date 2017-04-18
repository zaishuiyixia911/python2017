#!/usr/bin/python
#_*_ coding:utf-8 _*_

import urllib,urllib2
import cookielib
import re

class ChenkOn(object):
	def __init__(self):
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
		self.baseURL = 'http://tech.gopay.com.cn/login?back_url=http://tech.gopay.com.cn/my/page'
		self.baseURL1 = 'http://tech.gopay.com.cn'
		self.loginURL = 'http://tech.gopay.com.cn/login'
		self.checkonURL = 'http://tech.gopay.com.cn/k_attrecords/show_one'
	
	def getPage(self):
		self.cookie = cookielib.CookieJar()
		handler = urllib2.HTTPCookieProcessor(self.cookie)
		self.opener = urllib2.build_opener(handler)
		try:
			request = urllib2.Request(url=self.baseURL1,headers=self.headers)
			response = self.opener.open(request)
			return response.read()
		except urllib2.URLError,e:
			if hasattr(e,'code'):
				print "连接服务器失败，错误代码",e.code
				return None
			if hasattr(e,'reason'):
				print "连接服务器失败，错误原因",e.reason 
				return None

	def getToken(self):
		page = self.getPage()
		re_token = re.compile(r'<form.*?<input.*?value="(.*?)".*?>',re.S)
		token = re_token.search(page)
		if token:
			return token.group(1)
		else:
			return None

	def login(self):
		data = {"authenticity_token":self.getToken(),
			"username":"shaohongshuai",
			"password":"yeruiliang911",
			"login":""}
		self.postdata = urllib.urlencode(data)
		try:
			request = urllib2.Request(url=self.loginURL,
						  data=self.postdata,
						  headers=self.headers)
			response = self.opener.open(request)
			request1 = urllib2.Request(url=self.checkonURL,headers=self.headers)
			response1 = self.opener.open(request1)
			html = response1.read()
			return html
		except urllib2.URLError,e:
			if hasattr(e,'code'):
				print "连接服务器失败，错误代码",e.code
				return None
			if hasattr(e,'reason'):
				print "连接服务器失败，错误原因",e.reason 
				return None

	def getContent(self):
		html = self.login()
		re_html = re.compile(r'<tr class.*?<td>(.*?)</td.*?<td>(.*?)</td.*?<td>(.*?)</td.*?<td>(.*?)</td.*?<td>(.*?)</td>',re.S)
		items = re_html.findall(html)
       		page_contents = []
		print "员工姓名\t日期\t\t星期\t\t上班时间\t下班时间\n"
       		for item in items:
                	page_contents.append([item[0].strip().split("&")[0],
                        	              item[1].strip().split("&")[0],
                                	      item[2].strip().split("&")[0],
					      item[3].strip().split("&")[0],
					      item[4].strip().split("&")[0]])
#	        return page_contents

		for page in page_contents:
                        print "%s\t\t%s\t%s\t\t%s\t\t%s\n" %(page[0],page[1],page[2],page[3],page[4])

co = ChenkOn()
co.getToken()
co.getContent()	
