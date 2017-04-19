#!/usr/bin/python

import os
import sys
import hashlib

def md5sum(f):
        md5 = hashlib.md5()
        fd = open(f)
        while True:
                data = fd.read(1024*4)
                if data:
                        md5.update(data)
                else:
                        break
        fd.close()
        return md5.hexdigest()

def gen_dic(topdir):
	dic = {}
	a = os.walk(topdir)
	for p,d,f in a:
		for i in f:
			md5 = md5sum(os.path.join(p,i))
			fn = os.path.join(p,i)
			if dic.has_key(md5):
				dic[md5].append(fn)
			else:
				dic[md5] = [fn]
	return dic

if __name__ =='__main__':
	dic = gen_dic(sys.argv[1])
	for key,value in dic.items():
		if len(value) > 1: 
			print key,value
