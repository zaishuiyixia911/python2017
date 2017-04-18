#!/usr/bin/python
#_*_ coding:utf-8 _*_

import urllib, urllib2
import re
import sys

def getPage(page_num=1):
	url = 'http://www.cnnvd.org.cn/vulnerability/index/p/' + str(page_num)
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
	re_page = re.compile(r'<td width="15%.*?<a href="(.*?)" title="(.*?)">.*?<td width="45%.*?<a href=".*?" title="(.*?)">.*?<td width="15%" .*?>(.*?)</td>',re.S)
	items = re_page.findall(html)
	page_contents = []
	for item in items:
		index = "http://www.cnnvd.org.cn"
		index = index + item[0] 
		page_contents.append([page_num,
				     index.strip(),
				     item[1].strip(),
				     item[2].strip(),
				     item[3].strip()])
	return page_contents

def getOneStory(page_contents):
                input = raw_input()
                if input == 'Q' or input == 'q':
                        sys.exit()
        	for page in page_contents:
               	        print "页面:%s\n漏洞链接:%s\n漏洞编号:%s\n漏洞名称:%s\n发布时间:%s\n" %(page[0],page[1],page[2],page[3],page[4])
		

if __name__ == '__main__':
        print "正在读取漏洞列表，按回车看下一页，退出(Q|q)"
        num = 1
        while True:
                page_contents = getPageContent(num)
                getOneStory(page_contents)
                num += 1

