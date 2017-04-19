#!/usr/bin/python
# _*_ coding:utf-8 _*_

import urllib
import re
import time
import os

def schedule(a,b,c):
	per = 100.0*a*b/c
	if per >100:
		per = 100
	print '%.2f%%' %per

def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def downloadImg(htm):
	re_img = re.compile(r'<img class="BDE_Image" src="(.*?)".*?>')
	img_list = re_img.findall(html)
	t = time.localtime(time.time())
	foldername = str(t.__getattribute__("tm_year"))+"-"+str(t.__getattribute__("tm_mon"))+"-"+str(t.__getattribute__("tm_mday")) 
	picpath = '/home/shao/python/exercise/spider/image/%s/' %foldername
	print picpath
#	picpath = '/home/shao/python/exercise/spider/image/'
	
	if not os.path.exists(picpath):
		os.makedirs(picpath)

	x=0
	for imgurl in img_list:
		target = picpath + '%s.jpg' %x
		print 'Downloading image to location: ' + target + '\nurl=' + imgurl
		image = urllib.urlretrieve(imgurl, target, schedule)
		x=x+1
	return image

if __name__ == '__main__':
	html = getHtml('http://tieba.baidu.com/p/4951216775')
	downloadImg(html)
	print 'Download has finished'
