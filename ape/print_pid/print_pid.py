#!/usr/bin/python

import sys
import os

def isNum(s):
	if i.isdigit():
		return True
	return False

for i in os.listdir("/proc"):
	if isNum(i):
		print i
