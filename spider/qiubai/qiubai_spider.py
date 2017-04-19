#!/usr/bin/python
#_*_ coding:utf-8 _*_

import urllib, urllib2
import re
import sys

def getPage(page_num=1):
	url = 'http://www.qiushibaike.com/8hr/page/' + str(page_num)
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
	try:
		request = urllib2.Request(url,headers=headers)
		response = urllib2.urlopen(request)
		html = response.read()
		return html
	except urllib2.URLError,e:
		if hasattr(e,"code"):
			print "连接服务器失败，错误代码：%s" %e.code
			return None
		if hasattr(e,"reason"):
			print "连接服务器失败，错误原因：%s" %e.reason
			return None

def getPageContent(page_num=1):
	html = getPage(page_num)
	re_page = re.compile(r'<div class="author.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<i class="number">(\d+)</i>',re.S)
	items = re_page.findall(html)
	page_contents = []
	for item in items:
		replaceBR = re.compile(r'<br/>')
		new_content = replaceBR.sub('\n',item[1])
		page_contents.append([page_num,
				     item[0].strip(),
				     new_content.strip(),
				     item[2].strip()])
	return page_contents
def getOneStory(page_contents):
	for story in page_contents:
		input = raw_input()
		if input == 'Q' or input == 'q':
			sys.exit()
		print "第%d页\t发布人:%s\t赞:%s\n%s\n" %(story[0],story[1],story[3],story[2])

if __name__ == '__main__':
	print "正在读取段子，按回车看新段子，退出(Q|q)"
	num = 1
	while True:
		page_contents = getPageContent(num)
		getOneStory(page_contents)
		num += 1

