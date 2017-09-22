#!/usr/bin/python
#_*_ coding:utf-8 _*_
#####################read me##################
#我们使用的是列表转换成字典时的一个特点，即字典的key相同时，会丢掉value小的值。
#如list1 = [('a',2),('a',5)] ，转成成字典后,dict(list1) 为{'a': 5}
#但是58.19.224.0/19和58.19.224.0/22，我们要保留58.19.224.0/19，所以我们可以对掩码做一次差值，即32-掩码，等生成字典后，再取一次差值，再用32-掩码
##################### 实现功能  #################
#该程序能对ip组实现去重功能，ip包括精确ip、ip段、带掩码的ip，默认是一行一个ip组
#执行时使用 python parse_ip.py ip列表文件1 ip列表文件2
#具体的ip与ip段的合并，已经解决，用的是将ip转换成网络字节序，格式如下
#socket.inet_ntoa(struct.pack("!I",struct.unpack("!I",socket.inet_aton('精确ip'))[0] & struct.unpack("!I",socket.inet_aton('掩码'))[0]))

from optparse import OptionParser
import os,sys
import socket,struct

def opt():
	parser = OptionParser()
	options ,args = parser.parse_args()
	return options,args

def ParseList(data):
	list1 = []  #存放精确和ip段
	list2 = []  #存放带掩码的ip
	data = str(data).split('\n')[:-1]     #将获取的数据按行，分割成列表
	for i in data:
		if '/' not in i and '-' not in i:   #如果为精确ip，如：58.19.0.13，我们给他加一个32位的掩码
			t = (i)
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
					t = (real_ip)             
					#print t                        
					list1.append(t)                 #追加到列表里
			else:     #如果ip段的格式为：58.19.160.9 - 58.19.160.15，其中b=58.19.160.15
				pre_a = '.'.join(a.split(".")[:-1])+"."   #取a(58.19.160.9)的前缀58.19.160.
				last_a = int(a.split(".")[-1])            #取a的后缀
				last_b = int(b.split(".")[-1])            #取b的后缀
				for node in range(last_a,int(last_b)+1):
					real_ip =  pre_a + str(node)
                                        t = (real_ip)
                                        #print t
					list1.append(t)                  #追加列表
				
		else:
			if int(i.split('/')[1]) == 32:    #如果掩码是32，也保存到list1,list2只保存带掩码的且掩码非32
				list1.append(t)
			else:
			        t = (i.split('/')[0],str(32-int(i.split('/')[1]))) #如果是带掩码的ip，按'/'分割，并对掩码做一次差值
				list2.append(t)
				dic1 = dict(list2)
				list2 = dic1.items()
	new_list = []
        for i in list2:
               t = i[0]+"/"+str(32-int(i[1]))  #对列表掩码再做一次差值
               new_list.append(t)
	list2 = new_list
	print
	print "#"*80
	print "		Output information is as follows:"
	print
	print "		the count of old_list is:" + str(len(list1+list2))
	print
	t = 0
	for i in list1:   #将精确ip与带掩码的ip用ip_in_subnet函数计算
		for j in list2:
			if ip_in_subnet(i,j): #如果ip属于ip段，退出本循环，比较下一个精确ip
				break
			else:
				t=t+1     #如果ip不属于ip段1，则让ip与ip段2做比较，并将计数器+1，当ip不属于所有的ip段时，将该ip写入列表
				continue
		if t == len(list2):
			list2.append(i)
		t = 0  #重置计数器
	list2 = list(set(list2))
	print "		the count of new_list is:" +str(len(list2))
	#print "the new list2"
	#print list2
	print

	with open('/tmp/list1.txt','w') as fd:   #写到文件里
		for i in list2:
       			fd.write(str(i+'\n'))
	print "		the new ip_list is write in the /tmp/list1.txt "
	print
	print "#"*80
	print
	return list2

def format_subnet(subnet_input):
    # 如果输入的ip，将掩码加上后输出  
    if subnet_input.find("/") == -1:
        return subnet_input + "/255.255.255.255"

    else:
        # 如果输入的是短掩码，则转换为长掩码  
        subnet = subnet_input.split("/")
        if len(subnet[1]) < 3:
            mask_num = int(subnet[1])
            last_mask_num = mask_num % 8
            last_mask_str = ""
            for i in range(last_mask_num):
                last_mask_str += "1"
            if len(last_mask_str) < 8:
                for i in range(8-len(last_mask_str)):
                    last_mask_str += "0"
            last_mask_str = str(int(last_mask_str,2))
            if mask_num / 8 == 0:
                subnet = subnet[0] + "/" + last_mask_str +"0.0.0"
            elif mask_num / 8 == 1:
                subnet = subnet[0] + "/255." + last_mask_str +".0.0"
            elif mask_num / 8 == 2 :
                subnet = subnet[0] + "/255.255." + last_mask_str +".0"
            elif mask_num / 8 == 3:
                subnet = subnet[0] + "/255.255.255." + last_mask_str
            elif mask_num / 8 == 4:
                subnet = subnet[0] + "/255.255.255.255"
            subnet_input = subnet

        # 计算出正确的子网地址并输出  
        subnet_array = subnet_input.split("/")
        subnet_true = socket.inet_ntoa(struct.pack("!I",struct.unpack("!I",socket.inet_aton(subnet_array[0]))[0] & struct.unpack("!I",socket.inet_aton(subnet_array[1]))[0])) + "/" + subnet_array[1]
        return subnet_true

# 判断ip是否属于某个网段  
def ip_in_subnet(ip,subnet):
    subnet = format_subnet(str(subnet))
    subnet_array = subnet.split("/")
    ip = format_subnet(ip + "/" + subnet_array[1])
    return ip == subnet

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
