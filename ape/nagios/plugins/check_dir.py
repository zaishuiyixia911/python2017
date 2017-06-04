#!/usr/bin/python

from optparse import OptionParser
import sys
from subprocess import Popen,PIPE
import shlex
import datetime
import operator
import re
import os


def opt():
        parser = OptionParser("Usage: %prog [-w WARNING] [-c CRITICAL]")
        parser.add_option('-w',
                          dest='warning',
                          action='store',
                          default=1,
                          help='WARNING')
        parser.add_option('-c',
                          dest='critical',
                          action='store',
                          default=5,
                          help='CRITICAL')
        options, args = parser.parse_args()
        return options, args


def parsedir(data):
#	a = os.walk(sys.argv[1])
	a = os.walk(data)
	n = 0
	for p,d,f in a:
	        os.chdir(p)
	        p1 = Popen(['ls','-l'],stdout=PIPE)
	        p2 = Popen(['grep','root'],stdin=p1.stdout,stdout=PIPE)
	        result = p2.stdout
	        for i in  result:
	#		print os.path.join(p,i)
	 #               print i,
	                n += 1
	return n


def main():
	p = Popen(['date'],stdin=PIPE,stdout=PIPE,stderr=PIPE)
	time = p.stdout.read().split()
	year = time[0][:4]
	month = time[1][:2]
	day = time[2][:2]
	options, args = opt()
	w = int(options.warning)
	c = int(options.critical)
        data = '/usr/local/ciecc/webapps/upload/excelsave/'+year+'/'+month+'/'+day
#	print data
        num =  parsedir(data)
	if num < w:
		print "OK! "+"there is no root permission file,the num is:",num
		sys.exit(0)
	elif w <= num < c:
		print "WARNING! "+"/usr/local/ciecc/webapps/upload has root permission file, the num is:" ,num
		sys.exit(1)
	elif num >= c:
		print "CRITICAL! "+"/usr/local/ciecc/webapps/upload has root permission file, the num is:" ,num
		sys.exit(2)
	else:
		print "UNKNOWN",num
		sys.exit(3)

if __name__ == '__main__':
	main()
