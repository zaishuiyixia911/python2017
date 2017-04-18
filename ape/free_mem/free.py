#!/usr/bin/python

with open("/proc/meminfo") as fd:
	for line in fd:
		if line.startswith("MemTotal"):
			total=line.split()[1]
			continue
		if line.startswith("MemFree"): 
                        free=line.split()[1]
                       	break
print "total mem is: %.2f" %(int(total)/1024.0)+"M"
print "free  mem is: %.2f" %(int(free)/1024.0)+"M"
print "the percent is: %.2f" %(float(free)/float(total)*100)+"%"
