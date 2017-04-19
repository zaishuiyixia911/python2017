#!/usr/bin/python

import urllib,urllib2
from subprocess import Popen,PIPE

def getDmi():
	p = Popen(['dmidecode'],stdout=PIPE)
	data = p.stdout
	lines = []
	dmi = {}
	a = True
	while a:
	        line = data.readline()
	        if line.startswith('System Information'):
	                while True:
	                        line = data.readline()
	                        if line == '\n':
	                                a = False
	                                break
	                        else:
	                                lines.append(line)
	
	dmi_dic = dict([i.strip().split(':') for i in lines])
	dmi['Manufacturer'] = dmi_dic['Manufacturer'].strip()
	dmi['Product'] = dmi_dic['Product Name'].strip()
	dmi['serial'] = dmi_dic['Serial Number'].strip()
	return dmi

def getIfconfig():
        p = Popen(['ifconfig'],stdout=PIPE)
        data = p.stdout.read().split('\n\n')
        return [i for i in data if i and i.startswith('br')]

def parseIfconfig(data):
        dic = {}
	name = 'ip'
        for lines in data:
                line_list = lines.split('\n')
                devname = line_list[0].split()[0]
                macaddr = line_list[0].split()[-1]
                ipaddr = line_list[1].split()[1].split(':')[1]
                dic[name] = ipaddr
        return dic

def getHost():
	hn = "hostname"
	dic = {}
	p = Popen(['hostname'],stdout=PIPE)
	host = p.stdout.read().split('.')[1].strip()
	dic[hn] = host
	return dic
	
def getOsver():
	os = "os_version"
	dic = {}
	with open('/etc/issue') as fd:
		data = fd.read()
	version =  data.split('\n')[0]
	dic[os] = version
	return dic

def getCpuinfo():
	dic = {}
	cpu_num = "cpu_num"
	cpu_model = "cpu_model"
	i=0
	with open('/proc/cpuinfo') as fd:
		for line in fd:
			if line.startswith("model name"):
				model = line.split(':')[1].strip()
				continue
			if line.startswith("processor"):
				i += 1			
	dic[cpu_model] = model
	dic[cpu_num] = i
	return dic

def getMem():
	mem = "mem"
	dic = {}
	with open('/proc/meminfo') as fd:
		for line in fd:
			if line.startswith("MemTotal"):
				memsize = int(line.split()[1].strip())
				break
	memsize = "%s" % int(memsize/1024.0)+'M'
	dic[mem] = memsize
	return dic


if __name__ == '__main__':
	dict1 = {}
	data = getIfconfig()
	dic = parseIfconfig(data)
	dmi =  getDmi()
	host = getHost()
	os = getOsver()
	cpu = getCpuinfo()
	mem = getMem()
	dict1.update(dmi)
	dict1.update(host)
	dict1.update(os)
	dict1.update(cpu)
	dict1.update(mem)
	dict1.update(dic)
	print dict1
	#data = urllib.urlencode(dict1)
	#req = urllib2.urlopen('http://1.1.1.1:8000/hostinfo/collect/',data)
