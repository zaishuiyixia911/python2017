#!/usr/bin/python

from optparse import OptionParser
import os,sys

def opt():
	parser = OptionParser()
	options ,args = parser.parse_args()
	return options,args

def ParseList(data):
	list1 = []
	data = str(data).split('\n')[:-1]
	for i in data:
		if '/' not in i and '-' not in i:
			t = (i,'32')
			#print t
			list1.append(t)
		elif '-' in i:
			a,b = i.split('-')
			#print a,b
			if '.' not in b:
				pre_a = '.'.join(a.split(".")[:-1])+"."
				last_a = int(a.split(".")[-1])
				for node in range(last_a,int(b)+1):
					real_ip =  pre_a + str(node)
					t = (real_ip,'32')
					#print t
					list1.append(t)
			else:
				pre_a = '.'.join(a.split(".")[:-1])+"."
				last_a = int(a.split(".")[-1])
				last_b = int(b.split(".")[-1])
				for node in range(last_a,int(last_b)+1):
					real_ip =  pre_a + str(node)
                                        t = (real_ip,'32')
                                        #print t
					list1.append(t)
				
		else:
		        t = (i.split('/')[0],str(32-int(i.split('/')[1])))
			list1.append(t)
	#print list1
	print ("the count of old_list is",len(list1))
	dic1 = dict(list1)
	list2 = dic1.items()
	new_list = []
	for i in list2:
		t = i[0]+"/"+str(32-int(i[1]))
		new_list.append(t)
	print "remove the duplicate ip list, so we can get:"
	#print new_list
        print ("the count of new_list is",len(new_list))
	
	with open('/tmp/list1.txt','w') as fd:
		for i in new_list:
       			fd.write(str(i+'\n'))
	print "the new ip_list is write in the /tmp/list1.txt "
	return new_list

def main():
	list1 = []
	options,args = opt()
	for fn in args:
		if os.path.isfile(fn):
			with open(fn) as fd:
				data = fd.read()
  			list1.append(data)
		elif os.path.isdir(fn):
			print >> sys.stderr, "%s: is a directory" % fn
		else:
			sys.stderr.write("%s: No such file or directory\n" % fn)
	list1 = ''.join(list1)
        ParseList(list1)
		
if __name__ == '__main__':
	main()
