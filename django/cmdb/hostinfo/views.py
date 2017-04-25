from django.shortcuts import render
from hostinfo.models import Host,HostGroup
from django.http import HttpResponse
import pickle
import json

# Create your views here.

def collect(req):
	if req.POST:
		#obj =  pickle.loads(req.body)
		obj =  json.loads(req.body)
		hostname = obj['hostname']
		ip = obj['ip']
		Product = obj['Product']
		Manufacturer = obj['Manufacturer']
		serial = obj['serial']
		cpu_model = obj['cpu_model']
		cpu_num = obj['cpu_num']
		mem = obj['mem']
		os_version = obj['os_version']		
		
		try:
			host = Host.objects.get(serial=serial)
		except:
			host = Host()
		host.hostname = hostname
		host.ip = ip
		host.Product = Product
		host.Manufacturer = Manufacturer
		host.serial = serial
		host.cpu_model = cpu_model
		host.cpu_num = cpu_num
		host.mem = mem
		host.os_version = os_version
		host.save()
		return HttpResponse('OK')
	else:
		return HttpResponse('not data')

def getjson(req):
	ret_list = []
	hg = HostGroup.objects.all()
	for g in hg:
		ret = {'groupname':g.groupname,'members':[]}
		for h in g.members.all():
			ret_h = {'hostname':h.hostname,'ip':h.ip}
			ret['members'].append(ret_h)
		ret_list.append(ret)
	return HttpResponse(json.dumps(ret_list))

def gettxt(req):
	res = ' '
	hg = HostGroup.objects.all()
	for g in hg:
		groupname = g.groupname
		for h in g.members.all():
			hostname = h.hostname
			ip = h.ip
			res += groupname+' '+hostname+' '+ip+'\n'
	return HttpResponse(res)		












