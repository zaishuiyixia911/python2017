from django.db import models

# Create your models here.

class Host(models.Model):
	hostname = models.CharField(max_length=50)
	ip = models.IPAddressField()
	Product = models.CharField(max_length=50)
	Manufacturer = models.CharField(max_length=50)
	serial = models.CharField(max_length=50)
	cpu_model = models.CharField(max_length=50)
	cpu_num = models.IntegerField()
	mem = models.CharField(max_length=50)
	os_version = models.CharField(max_length=50)

	def __unicode__(self):
		return self.hostname
	
class HostGroup(models.Model):
	groupname = models.CharField(max_length=50)
	members = models.ManyToManyField(Host)
