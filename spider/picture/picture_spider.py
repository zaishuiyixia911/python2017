#!/usr/bin/python

import urllib, urllib2
import re

def getHtml(url):
	page = urllib2.urlopen(url)
	return page.read()

def getImage(html):
	re_img = re.compile(r'<img class="BDE_Image" src="(.*?)".*?>')
	img_list = re_img.findall(html)
	i = 1
	for imgurl in img_list:
		print imgurl
		urllib.urlretrieve(imgurl, filename="/home/shao/python/exercise/spider/image/%s.jpg" %i)
		i += 1

if __name__ == '__main__':
	url = 'http://tieba.baidu.com/p/4229162765'
	page = getHtml(url)
	img = getImage(page)
	
