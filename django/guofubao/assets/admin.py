#_*_coding:utf8_*_
from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from assets import models
from tasks.models import Task
from tasks.models import Branch

from django.contrib.auth import  forms as auth_form

from smtp import sendmail


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email','token')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password','is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email','is_admin','is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('department','tel','mobile','memo')}),
        ('API TOKEN info', {'fields': ('token',)}),
        ('Permissions', {'fields': ('is_active','is_admin')}),
        ('账户有效期', {'fields': ('valid_begin_time','valid_end_time')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2','is_active','is_admin')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class ServerInline(admin.TabularInline):
    model = models.Server
    exclude = ('memo',)
    #readonly_fields = ['create_date']

class CPUInline(admin.TabularInline):
    model = models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']
class NICInline(admin.TabularInline):
    model = models.NIC
    exclude = ('memo',)
    readonly_fields = ['create_date']
class RAMInline(admin.TabularInline):
    model = models.RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']
class DiskInline(admin.TabularInline):
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']

class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','asset_type','sn','name','manufactory','management_ip','idc','business_unit','admin','trade_date','status')
    inlines = [ServerInline,CPUInline,RAMInline,DiskInline,NICInline]
    search_fields = ['sn',]
    list_filter = ['idc','manufactory','business_unit','asset_type']
    choice_fields = ('asset_type','status')
    fk_fields = ('manufactory','idc','business_unit','admin')
    list_per_page = 10
    list_filter = ('asset_type','status','manufactory','idc','business_unit','admin','trade_date')
    dynamic_fk = 'asset_type'
    dynamic_list_display = ('model','sub_asset_type','os_type','os_distribution')
    dynamic_choice_fields = ('sub_asset_type',)
    m2m_fields = ('tags',)

class NicAdmin(admin.ModelAdmin):
    list_display = ('name','macaddress','ipaddress','netmask','bonding')
    search_fields = ('macaddress','ipaddress')


class EventLogAdmin(admin.ModelAdmin):
    list_display = ('name','colored_event_type','asset','component','detail','date','user')
    search_fields = ('asset',)
    list_filter = ('event_type','component','date','user')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('sn','time','serviceman','dpartment','responsibleman','dpartment1','task','taskman','tasktime','issue_des','issue_solve','feedback','leaderview','review')
    list_filter = ['sn','time','dpartment','taskman']
    search_fields = ['sn',]
    choice_fields = ('sn','time')
    fk_fields = ('sn','time','taskman','task')
    list_per_page = 10
    list_filter = ['sn','time','dpartment','taskman','task','review']
    dynamic_fk = 'sn'
    dynamic_choice_fields = ('sn',)
    actions = ['approve_selected_objects']
    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
	list1 = []
	for i in range(len(selected)):
	    obj = Task.objects.get(id=int(selected[i]))
	    obj.review = '已审核' 
	    obj.save()
	    send = "编号："+obj.sn + "<br/><br/><br/><br/>"+ "  工单时间： "+ str(obj.time) + "  服务对象： "+ obj.serviceman + "  所属部门： "+ obj.dpartment + "  工作负责人： "+ obj.responsibleman + "  所属部门： "+obj.dpartment1 + "  工作任务： "+ obj.task + "  任务签发人： "+ obj.taskman + "  签发时间： "+ str(obj.tasktime) + "   故障问题描述："+ obj.issue_des + "  故障解决情况： "+ obj.issue_solve + "  审核情况： "+ obj.review 

	    print send
	    print obj.review
	    print ("obj",obj) 
	sendmail(send)
    approve_selected_objects.short_description = "审核所选的 故障表"

class BranchAdmin(admin.ModelAdmin):
    list_display = ('sn','serviceman','time','operation','content','operaman','developman','review','solve')

    list_filter = ['sn','time','serviceman','operation','operaman']
    search_fields = ['sn',]
    choice_fields = ('sn','time')
    fk_fields = ('sn','time','operation','operaman')
    list_per_page = 10
    dynamic_fk = 'sn'
    dynamic_choice_fields = ('sn',)
    actions = ['approve_selected_objects','operate_selected_objects']
    def approve_selected_objects(modeladmin, request, queryset):
        blank = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        for i in range(len(selected)):
            obj = Branch.objects.get(id=int(selected[i]))
            obj.review = '已审核'
            obj.save()
	    list1 = obj.content.split('\n')
	    str1=""
	    for i in range(len(list1)):
		str1=str1+list1[i]+"<br/>"+blank
	    print ("str1",str1)
            send = "编号："+obj.sn + "<br/>"  +blank+" 申请日期： "+ str(obj.time)+ "<br/>"  +blank+" 申请人： "+ obj.serviceman+ "<br/>"  + blank +"  所属部门： "+ obj.dpartment+ "<br/>"  +blank+ " 操作：" +obj.operation+ "<br/>"  +blank+" 分支或主干信息：" + str1+ " 操作人：" + obj.operaman+ "<br/>"  + blank+" 分支或主干所属人：" + obj.developman+ "<br/>"  + blank+" 申请原因：" + obj.branch_reason+ "<br/>"  +blank+ " 审核状态：" + obj.review+ "<br/>"  + blank+" 执行状态：" + obj.solve+ "<br/>" 

            print send
    	    print "******************************分支或主干信息************************"
	    print obj.content
	    list1 = obj.content.split('\n')
	    print ("list1",list1)
	    print type(obj.content)
            print obj.review
            print ("obj",obj)
        sendmail(send)
    def operate_selected_objects(modeladmin, request, queryset):
	pass
    approve_selected_objects.short_description = "审核所选的 发布表"
    operate_selected_objects.short_description = "执行所选的 发布表"


from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect




class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ('sn','asset_type','manufactory','model','cpu_model','cpu_count','cpu_core_count','ram_size','os_distribution','os_release','date','approved','approved_by','approved_date')
    actions = ['approve_selected_objects']
    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    approve_selected_objects.short_description = "批准入库"

# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)
admin.site.register(models.Asset,AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.NetworkDevice)
admin.site.register(models.IDC)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Contract)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.NIC,NicAdmin)
admin.site.register(models.RAM)
admin.site.register(models.Manufactory)
admin.site.register(models.Tag)
admin.site.register(models.Software)
admin.site.register(models.EventLog,EventLogAdmin)
admin.site.register(models.NewAssetApprovalZone,NewAssetApprovalZoneAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Branch,BranchAdmin)
#admin.site.register(models.Task,TaskAdmin)
