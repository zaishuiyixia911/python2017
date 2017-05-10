#!/usr/bin/python

from optparse import OptionParser
import sys

unit = {'b':1, 'k':2**10, 'm':2**20, 'g':2**30, 't':2**40}

def opt():
	parser = OptionParser("Usage: %prog [-w WARNING] [-c CRITICAL]")
	parser.add_option('-w',
			  dest='warning',
			  action='store',
			  default='50',
			  help='WARNING')
	parser.add_option('-c',
			  dest='critical',
			  action='store',
			  default='30',
			  help='CRITICAL')
	options, args = parser.parse_args()
	return options, args

def getMem(f):
	with open(f) as fd:
		for line in fd:
			if line.startswith('MemFree'):
				mem = line.split()[1].strip()
				break
	return int(mem) * 1024

def scaleUnit(s):
	lastchar = s[-1]
	lastchar = lastchar.lower()
	num = float(s[:-1])
	if lastchar in unit:
		return num * unit[lastchar]
	else:
		return int(s)

def change(byte):
	for k, v in unit.items():
		num = float(byte)/v
		if 1 < num <=1024:
			num = "%.2f" %num
			result = str(num) + k.upper()
	return result	

def main():
	options, args = opt()
        w =  scaleUnit(options.warning)
        c =  scaleUnit(options.critical)
	mem = getMem('/proc/meminfo')
	h_read = change(mem)
	if mem > w:
		print "OK",h_read
		sys.exit(0)
	elif c < mem <= w:
		print "WARNING",h_read
		sys.exit(1)
	elif mem < c:
		print "CRITICAL",h_read
		sys.exit(2)
	else:
		print "UNKNOWN",h_read
		sys.exit(3)


if __name__ == '__main__':
	main()
