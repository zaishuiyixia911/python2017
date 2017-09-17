#!/usr/bin/python
#_*_ coding:utf-8 _*_
#####################read me##################
#我们使用的是列表转换成字典时的一个特点，即字典的key相同时，会丢掉value小的值。
#如list1 = [('a',2),('a',5)] ，转成成字典后,dict(list1) 为{'a': 5}
#但是58.19.224.0/19和58.19.224.0/22，我们要保留58.19.224.0/19，所以我们可以对掩码做一次差值，即32-掩码，等生成字典后，再取一次差值，再用32-掩码
##################### 实现功能  #################
#该程序能对ip组实现去重功能，ip包括精确ip、ip段、带掩码的ip，默认是一行一个ip组
#执行时使用 python parse_ip.py ip列表文件1 ip列表文件2
#未完成，未实现一个具体的ip与ip段的合并，这个要用到求与操作，有时间去做

from optparse import OptionParser
import os,sys

def opt():
	parser = OptionParser()
	options ,args = parser.parse_args()
	return options,args

def ParseList(data):
	list1 = []
	data = str(data).split('\n')[:-1]     #将获取的数据按行，分割成列表
	for i in data:
		if '/' not in i and '-' not in i:   #如果为精确ip，如：58.19.0.13，我们给他加一个32位的掩码
			t = (i,'0')
			#print t
			list1.append(t)   #追加到列表里
		elif '-' in i:            #如果是ip段
			a,b = i.split('-')   #将ip段按照'-'分割成两部分
			#print a,b
			if '.' not in b:    #如果ip段的格式为：58.19.128.1 - 10，其中b=10
				pre_a = '.'.join(a.split(".")[:-1])+"." #取a(58.19.128.1)的前缀58.19.128.
				last_a = int(a.split(".")[-1])          #取a(58.19.128.1)的后缀1
				for node in range(last_a,int(b)+1):     # for i in range(1,10+1)
					real_ip =  pre_a + str(node)    
					t = (real_ip,'0')             
					#print t                        
					list1.append(t)                 #追加到列表里
			else:     #如果ip段的格式为：58.19.160.9 - 58.19.160.15，其中b=58.19.160.15
				pre_a = '.'.join(a.split(".")[:-1])+"."   #取a(58.19.160.9)的前缀58.19.160.
				last_a = int(a.split(".")[-1])            #取a的后缀
				last_b = int(b.split(".")[-1])            #取b的后缀
				for node in range(last_a,int(last_b)+1):
					real_ip =  pre_a + str(node)
                                        t = (real_ip,'0')
                                        #print t
					list1.append(t)                  #追加列表
				
		else:
		        t = (i.split('/')[0],str(32-int(i.split('/')[1]))) #如果是带掩码的ip，按'/'分割，并对掩码做一次差值
			list1.append(t)
	#print list1
	print ("the count of old_list is",len(list1))
	dic1 = dict(list1)                 #将列表生成字典，key相同时，去掉value小的值
	list2 = dic1.items()               #将字典生成列表
	new_list = []
	for i in list2:
		t = i[0]+"/"+str(32-int(i[1]))  #对列表掩码再做一次差值
		new_list.append(t)
	print "remove the duplicate ip list, so we can get:"
	#print new_list
        print ("the count of new_list is",len(new_list))
	
	with open('/tmp/list1.txt','w') as fd:   #写到文件里
		for i in new_list:
       			fd.write(str(i+'\n'))
	print "the new ip_list is write in the /tmp/list1.txt "
	return new_list

def main():
	list1 = []
	options,args = opt()
	if not args:
		print ""
		print "follow this:"
		print "python parse_ip.py ip列表1 ip列表2 ....(脚本后面可以跟1个或多个文件) "
		print ""
		exit(0)
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
