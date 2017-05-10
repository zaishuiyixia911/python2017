#!/usr/bin/python

from optparse import OptionParser
import sys
from subprocess import Popen,PIPE
import shlex
import datetime
import operator
import re

LOG_REG = re.compile(r'(?P<logtime>\w{3}\s{1,2}\d{1,2}\s[\d:]{8})\s(?P<hostname>[\w\.]+)\s(?P<program>\w+(\[\d+\])?):\s(?P<msg>.*)')

MONTH = {
	'Jan':1,
	'Feb':2,
	'Mar':3,
	'Apr':4,
	'May':5,
	'Jun':6,
	'Jul':7,
	'Aug':8,
	'Sep':9,
	'Oct':10,
	'Nov':11,
	'Dec':12}

def opt():
        parser = OptionParser("Usage: %prog [-w WARNING] [-c CRITICAL]")
        parser.add_option('-w',
                          dest='warning',
                          action='store',
                          default=5,
                          help='WARNING')
        parser.add_option('-c',
                          dest='critical',
                          action='store',
                          default=10,
                          help='CRITICAL')
        options, args = parser.parse_args()
        return options, args

def getLog(f,n):
	cmd = 'tail -n %s %s' %(n,f)
	p = Popen(shlex.split(cmd),stdout=PIPE,stderr=PIPE)
	stdout,stderr = p.communicate()
	return stdout	

def parseLogTime(line):
	now = datetime.datetime.now()
	month,day,time = line.split()[:3]
	hour,minute,second = [int(i) for i in time.split(':')]
	logtime = datetime.datetime(now.year,MONTH[month],int(day),hour,minute,second)
	print str(logtime)+"logtime"
	return logtime

def countDict(k,d):
	if k in d:
		d[k] += 1
	else:
		d[k]=1

def parseLog(data):
	dic = {}
	now = datetime.datetime.now()
	ten_m_ago = now - datetime.timedelta(minutes=3000)
	print str(ten_m_ago)+"ten_m_ago"
	data = [i for i in data.split('\n') if i]
	for line in data:
		logtime = parseLogTime(line)
		if logtime > ten_m_ago:
			match = LOG_REG.search(line)
			if match:
				match_dic = match.groupdict()
				k = str(logtime)+' '+match_dic['program']
				if 'warning' in match_dic['msg'].lower():
					countDict(k,dic)
	return dic	

def main():
	p = Popen('whoami',stdout=PIPE,shell=True)
	user = p.stdout.read()
	options, args = opt()
	w = int(options.warning)
	c = int(options.critical)
	lines = c * 600
        data = getLog('/var/log/messages',lines)
        dic =  parseLog(data)
	if not dic:
		print "OK,the message is empty"
		sys.exit(0)
	sorted_dic = sorted(dic.iteritems(),key=operator.itemgetter(1),reverse=True)
	num =  sorted_dic[0][1]
	if num < w:
		print "OK",sorted_dic[0],user
		sys.exit(0)
	elif w <= num < c:
		print "WARNING",sorted_dic[0],user
		sys.exit(1)
	elif num >= c:
		print "CRITICAL",sorted_dic[0],user
		sys.exit(2)
	else:
		print "UNKNOWN",sorted_dic[0],user
		sys.exit(3)

if __name__ == '__main__':
	main()
