#_*_ coding:utf-8 _*_

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

from assets.myauth import UserProfile
from assets import models
from django.db import models

# Create your models here.

class Task(models.Model):
    sn = models.CharField('编号',max_length=50)
    time = models.DateField(u'工单日期',null=True, blank=True)
    serviceman = models.CharField('服务对象',max_length=50)
    dpartment = models.CharField('所属部门',max_length=50)
    dpartment_type_choices = (
        ('tech', u'技术研发部'),
        ('admin', u'人资行政部'),
        ('finance', u'计划财务部'),
        ('operation', u'运营支持部'),
        ('risk', u'风险控制部'),
        ('bank', u'金融服务部'),
        ('cross', u'跨境支付项目组'),
        ('move', u'移动支付项目组'),
        ('net', u'网络支付部'),
        ('others', u'其它部门'),
    )
    dpartment = models.CharField('所属部门',choices=dpartment_type_choices,max_length=64, default='tech')
    responsibleman = models.CharField('工作负责人',max_length=50)
    dpartment1 = models.CharField('所属部门',choices=dpartment_type_choices,max_length=64, default='tech')
    task = models.CharField('工作任务',max_length=200)
    taskman = models.CharField('工作任务签发人',max_length=50)
    tasktime = models.DateField(u'签发时间',null=True, blank=True)
    issue_des = models.CharField('故障问题描述',max_length=200)
    issue_solve = models.CharField('故障解决情况',max_length=50)
    feedback = models.CharField('服务反馈意见',max_length=50)
    leaderview = models.CharField('领导意见',max_length=50)	
    review = models.CharField('审核状态',max_length=50,default='未审核',editable=False)
    #approved = models.BooleanField(u'已批准',default=False)
    #approved_by = models.ForeignKey('UserProfile',verbose_name=u'批准人',blank=True,null=True)
    #approved_date = models.DateTimeField(u'批准日期',blank=True,null=True)

    class Meta:
        verbose_name = '故障表'
        verbose_name_plural = "故障表"
    def __str__(self):
        return '<id:%s task:%s>'  %(self.id,self.task )

class Branch(models.Model):
    sn = models.CharField('编号',max_length=50)
    time = models.DateField(u'申请日期',null=True, blank=True)
    serviceman = models.CharField('申请人',max_length=50)
    dpartment = models.CharField('所属部门',max_length=50)
    dpartment_type_choices = (
        ('tech', u'技术研发部'),
        ('admin', u'人资行政部'),
        ('finance', u'计划财务部'),
        ('operation', u'运营支持部'),
        ('risk', u'风险控制部'),
        ('bank', u'金融服务部'),
        ('cross', u'跨境支付项目组'),
        ('move', u'移动支付项目组'),
        ('net', u'网络支付部'),
        ('others', u'其它部门'),
    )
    dpartment = models.CharField('所属部门',choices=dpartment_type_choices,max_length=64, default='tech')
    #responsibleman = models.CharField('直属领导',max_length=50)
    #dpartment1 = models.CharField('所属部门',choices=dpartment_type_choices,max_length=64, default='tech')
    operation_type_choices = (
        ('branch.py', u'打分支'),
        ('branches_merge.py', u'合分支'),
        ('trunk_merge.py', u'合主干'),
        ('pretrunk_merge.py', u'预主干'),
    )
    operation = models.CharField('操作',choices=operation_type_choices,max_length=64,default='branch')
    content = models.TextField('分支或主干信息',max_length=300)
    operaman_type_choices = (
        ('zjc', u'张金超'),
        ('changlh', u'常龙欢'),
        ('liwei', u'李伟'),
    )
    operaman = models.CharField('操作人',choices=operaman_type_choices,max_length=64,default='zjc')
    developman_type_choices = (
        ('lilili', u'栗丽丽'),
        ('qianlidong', u'钱立冬'),
        ('xuanguanghai', u'宣广海'),
    )
    developman = models.CharField('分支或主干所属人',choices=developman_type_choices,max_length=64,default='lilili')
    branch_des = models.CharField('描述',max_length=200,null=True, blank=True)
    branch_reason = models.CharField('申请原因',max_length=200,null=True, blank=True)
#    feedback = models.CharField('服务反馈意见',max_length=50)
 #   leaderview = models.CharField('领导意见',max_length=50)
    review = models.CharField('审核状态',max_length=50,default='未审核',editable=False)
    solve = models.CharField('执行状态',max_length=50,default='未执行',editable=False)

    class Meta:
        verbose_name = '发布表'
        verbose_name_plural = "发布表"
    def __str__(self):
        return '<id:%s operation:%s>'  %(self.id,self.operation )

