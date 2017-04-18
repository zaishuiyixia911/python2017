#!/usr/bin/python
#_*_ coding:utf-8 _*_
#writen by shs at 2017-02-27


from optparse import OptionParser
import sys


def opt():
	parser = OptionParser()
	parser.add_option("-p","--plus",
			  dest="pluses",
			  action="store_true",
			  default=False,
			  help="only conut plus")
	parser.add_option("-m","--minus",
			  dest="minuses",
			  action="store_true",
			  default=False,
			  help="only conut minus")
	parser.add_option("-t","--time",
			  dest="timeses",
			  action="store_true",
			  default=False,
			  help="only count multiply")
	parser.add_option("-d","--divide",
			  dest="divides",
			  action="store_true",
			  default=False,
			  help="only count divide")
	options ,args = parser.parse_args()
	return options,args

def print_count(options,pluses,minuses,timeses,divides,*num):
	i = 0
	length = len(num) -2
	if options.pluses:
		t = "+".join(num)
		num1 = [int(j) for j in num]
		sum = num1[i] + num1[i+1]
		while length:
			i = i+1
			sum = sum  + num1[i+1] 
			length = length - 1
		print "%s = %s" %(t,sum)
	i = 0
        length = len(num) -2
	if options.minuses:
		t = "-".join(num)
		num2 = [int(j) for j in num]
		sum = num2[i] - num2[i+1]
		while length:
			i = i+1
			sum = sum  - num2[i+1] 
			length = length - 1
		print "%s = %s" %(t,sum)
	i = 0
        length = len(num) -2
	if options.timeses:
		t = "*".join(num)
		num3 = [int(j) for j in num]
		sum = num3[i] * num3[i+1]
                while length:
                        i = i+1
                        sum = sum  * num3[i+1]
                        length = length - 1
                print "%s = %s" %(t,sum)
	i = 0
        length = len(num) -2
	if options.divides:
		t = "/".join(num)
		num = [int(j) for j in num]
		sum = num[i] / num[i+1]
                while length:
                        i = i+1
                        sum = sum  / num[i+1]
                        length = length - 1
                print "%s = %s" %(t,sum)

def main():
	options,args = opt()
	if not (options.pluses or options.minuses or options.timeses or options.divides):
		options.pluses, options.minuses, options.timeses, options.divides = True, True, True, True
	if args:
		if len(args) == 1:
			print >> sys.stderr, "%s should have two  or more parameters" %__file__
			exit()
		pluses = options.pluses
		minuses = options.minuses
		timeses = options.timeses
		divides = options.divides
	        print_count(options,pluses,minuses,timeses,divides,*args)		
		
if __name__ == '__main__':
	main()
