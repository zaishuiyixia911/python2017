#_*_ coding:utf-8 _*_
from django.contrib import admin
from operation.models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
	list_display = [
		'sn',
                'time',
                'serviceman',
		'dpartment',
		'responsibleman',
		'dpartment1',
		'task',
		'taskman',
		'tasktime',
		'issue_des',
		'issue_solve',
		'feedback',
		'leaderview']	

admin.site.register(Task,TaskAdmin)
