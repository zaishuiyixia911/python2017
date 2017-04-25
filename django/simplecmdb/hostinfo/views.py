from django.shortcuts import render
from hostinfo.models import Host
from django.http import HttpResponse

# Create your views here.

def collect(req):
	if req.POST:
		hostname = req.POST.get('hostname')
		ip = req.POST.get('ip')
		Product = req.POST.get('Product')
		Manufacturer = req.POST.get('Manufacturer')
		serial = req.POST.get('serial')
		cpu_model = req.POST.get('cpu_model')
		cpu_num = req.POST.get('cpu_num')
		mem = req.POST.get('mem')
		os_version = req.POST.get('os_version')		
		
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
