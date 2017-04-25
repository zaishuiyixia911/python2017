from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader,Context
from blog.models import Host

# Create your views here.

def index(request):
	t = loader.get_template('index.html')
	c = Context({})
	return HttpResponse(t.render(c))


def db(req):
	print req
	if req.POST:
		hostname = req.POST.get('hostname')
		ip = req.POST.get('ip')
		host = Host()
		host.hostname = hostname
		host.ip = ip
		print host.hostname
		print host.ip
		host.save()
		return HttpResponse('OK')
	elif req.GET:
		hostname = req.GET.get('hostname')
		ip = req.GET.get('ip')
		host = Host()
		host.hostname = hostname
		host.ip = ip
		host.save()
		return HttpResponse('OK')
	else:
		return HttpResponse('not data')
