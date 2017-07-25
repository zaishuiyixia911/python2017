#!/usr/bin/python

from optparse import OptionParser
import sys
from subprocess import Popen,PIPE
import shlex
import datetime
import operator
import re

#LOG_REG = re.compile(r'(?P<logtime>\w{3}\s{1,2}\w{3}\s{1,2}\d{2}\s{1,2}[\d:]{8})\s.*?(?P<program>ORA-[\w\d]{1,10})\s.*')
LOG_REG = re.compile(r'(?P<logtime>\w{3}\s{1,2}\w{3}\s{1,2}\d{2}\s{1,2}[\d:]{8})\s.*?(?P<program>ORA-[\w\d\s\.\:]{4}).*')

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
                          default=1,
                          help='WARNING')
        parser.add_option('-c',
                          dest='critical',
                          action='store',
                          default=2,
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
	month,day,time = line.split()[1:4]
	hour,minute,second = [int(i) for i in time.split(':')]
	logtime = datetime.datetime(now.year,MONTH[month],int(day),hour,minute,second)
#	print str(logtime)+"logtime"
	return logtime

def countDict(k,d):
	if k in d:
		d[k] += 1
	else:
		d[k]=1

def parseLog(data):
	dic = {}
	list1 = []
	now = datetime.datetime.now()
	ten_m_ago = now - datetime.timedelta(minutes=5000)
	data = [i for i in data.split('2017\n') if i]
#	data[-1] = data[-1] +' '+ ' '.join(data[-2].split()[-3:])
#	data[0] = data[0]+' '.join(data[1].split('\n')[:-1])
	#list1.append(data[0])
	for i in range(2,len(data)):
		t=data[i-1].split('\n')[-1] + ' '.join(data[i].split('\n')[:-1])
		if str(t.split()[0]) in 'Mon|Tue|Wed|Thu|Fri|Sat|Sun':
#			print str(t.split()[0])
   	        	list1.append(t)
#	list1 = [i for i in list1 if i and str(i.split()[0]) in 'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'] 
	for line in list1:
		logtime = parseLogTime(line)
		if logtime > ten_m_ago:
                        match = LOG_REG.search(line)
                        if match:
                                match_dic = match.groupdict()
                                k = str(logtime)+' '+match_dic['program']
                                if 'ORA-' in line:
                                        countDict(k,dic)
	return dic	

def main():
	p = Popen('whoami',stdout=PIPE,shell=True)
	user = p.stdout.read()
	options, args = opt()
	w = int(options.warning)
	c = int(options.critical)
	lines = c * 600
        data = getLog('/home/shs/python/exercise/db-test/alert_test.log',lines)
#        data = getLog('/opt/pluings/aa.log',lines)
        dic =  parseLog(data)
	if not dic:
		print "OK,the 5 minute is no error message"
		sys.exit(0)
	sorted_dic = sorted(dic.iteritems(),key=operator.itemgetter(1),reverse=True)
	num =  sorted_dic[0][1]
	if num < w:
		print "OK",sorted_dic[0]
		sys.exit(0)
	elif w <= num < c:
		print "WARNING",sorted_dic[0]
		sys.exit(1)
	elif num >= c:
		print "CRITICAL",sorted_dic[0]
		sys.exit(2)
	else:
		print "UNKNOWN",sorted_dic[0]
		sys.exit(3)

if __name__ == '__main__':
	main()




