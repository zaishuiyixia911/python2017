#!/usr/bin/python
#_*_coding:utf8_*_

from django.shortcuts import render, HttpResponse
from assets import core, models, asset_handle, utils, admin
#from assets import core, models, admin
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from assets import tables
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from  assets.dashboard import  AssetDashboard
from tasks.models import Task,Branch

# Create your views here.


@login_required
def index(request):
    return render(request, 'index.html')


@csrf_exempt
@utils.token_required
def asset_report(request):
    print(request.GET)
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        if ass_handler.data_is_valid():
            print("----asset data valid:")
            ass_handler.data_inject()
            # return HttpResponse(json.dumps(ass_handler.response))

        return HttpResponse(json.dumps(ass_handler.response))
        # return render(request,'assets/asset_report_test.html',{'response':ass_handler.response})
        # else:
        # return HttpResponse(json.dumps(ass_handler.response))

    return HttpResponse('--test--')


@csrf_exempt
def asset_with_no_asset_id(request):
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        res = ass_handler.get_asset_id_by_sn()

        # return render(request,'assets/acquire_asset_id_test.html',{'response':res})
        return HttpResponse(json.dumps(res))


def new_assets_approval(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        approved_asset_list = request.POST.getlist('approved_asset_list')
        approved_asset_list = models.NewAssetApprovalZone.objects.filter(id__in=approved_asset_list)

        response_dic = {}
        for obj in approved_asset_list:
            request.POST['asset_data'] = obj.data
            ass_handler = core.Asset(request)
            if ass_handler.data_is_valid_without_id():
                ass_handler.data_inject()
                obj.approved = True
                obj.save()

            response_dic[obj.id] = ass_handler.response
        return render(request, 'assets/new_assets_approval.html',
                      {'new_assets': approved_asset_list, 'response_dic': response_dic})
    else:
        ids = request.GET.get('ids')
        id_list = ids.split(',')
        new_assets = models.NewAssetApprovalZone.objects.filter(id__in=id_list)
        return render(request, 'assets/new_assets_approval.html', {'new_assets': new_assets})


def asset_report_test(request):
    return render(request, 'assets/asset_report_test.html')


@login_required
def acquire_asset_id_test(request):
    return render(request, 'assets/acquire_asset_id_test.html')


@login_required
def asset_list(request):
    print(request.GET)
    asset_obj_list = tables.table_filter(request, admin.AssetAdmin, models.Asset)
    # asset_obj_list = models.Asset.objects.all()
    print("admin.AssetAdmin",admin.AssetAdmin)
    print("models.Asset",models.Asset)
    print("asset_obj_list_all",models.Asset.objects.all())
    print("asset_obj_list:", asset_obj_list)
    order_res = tables.get_orderby(request, asset_obj_list, admin.AssetAdmin)
    print('order-res----->',order_res)
    paginator = Paginator(order_res[0], admin.AssetAdmin.list_per_page)

    page = request.GET.get('page')
    try:
        asset_objs = paginator.page(page)
    except PageNotAnInteger:
        asset_objs = paginator.page(1)
    except EmptyPage:
        asset_objs = paginator.page(paginator.num_pages)

    table_obj = tables.TableHandler(request,
                                    models.Asset,
                                    admin.AssetAdmin,
                                    asset_objs,
                                    order_res
                                    )

    return render(request, 'assets/assets.html', {'table_obj': table_obj,
                                                  'paginator': paginator})


from assets import tables_task
@login_required
def task_list(request):
    print "%%%%%%%%%%%%%%%%%%%% request.GET %%%%%%%%%%%%%%%%%%%%%%"
    print(request.GET)
    task_obj_list = tables_task.table_filter(request, admin.TaskAdmin, Task)
    # asset_obj_list = models.Asset.objects.all()
    print("admin.TaskAdmin",admin.TaskAdmin)
    print("models.Task",Task)
    print("task_obj_list_all",Task.objects.all())
    print("task_obj_list:", task_obj_list)
    order_res = tables_task.get_orderby(request, task_obj_list, admin.TaskAdmin)
    print('task-list----->',order_res)
    paginator = Paginator(order_res[0], admin.TaskAdmin.list_per_page)

    page = request.GET.get('page')
    try:
        task_objs = paginator.page(page)
    except PageNotAnInteger:
        task_objs = paginator.page(1)
    except EmptyPage:
        task_objs = paginator.page(paginator.num_pages)

    table_obj = tables_task.TableHandler(request,
                                    Task,
                                    admin.TaskAdmin,
                                    task_objs,
                                    order_res
                                    )

    return render(request, 'assets/task.html', {'table_obj': table_obj,
                                                  'paginator': paginator})


from assets import tables_branch
@login_required
def branch_list(request):
    branch_obj_list = tables_branch.table_filter(request, admin.BranchAdmin, Branch)
    order_res = tables_branch.get_orderby(request, branch_obj_list, admin.BranchAdmin)
    paginator = Paginator(order_res[0], admin.BranchAdmin.list_per_page)
    print "shshSSSSSSSSSSSSSSSSSSSSSS   branch HHHHHHHHHHHHHHHHHHHHHHHHHHH"
    print("admin.TaskAdmin",admin.BranchAdmin)
    print("models.Branch",Branch)
    print("branch_obj_list_all",Task.objects.all())
    print("branch_obj_list:", branch_obj_list)
    page = request.GET.get('page')
    try:
        branch_objs = paginator.page(page)
    except PageNotAnInteger:
        branch_objs = paginator.page(1)
    except EmptyPage:
        branch_objs = paginator.page(paginator.num_pages)

    table_obj = tables_branch.TableHandler(request,
                                    Branch,
                                    admin.BranchAdmin,
                                    branch_objs,
                                    order_res
                                    )

    return render(request, 'assets/branch.html', {'table_obj': table_obj,
                                                  'paginator': paginator})


@login_required
def get_asset_list(request):
    asset_dic = asset_handle.fetch_asset_list()
    print(asset_dic)

    return HttpResponse(json.dumps(asset_dic, default=utils.json_date_handler))


@login_required
def asset_category(request):
    category_type = request.GET.get("category_type")
    print category_type
    if not category_type: category_type = 'server'
    if request.is_ajax():
        categories = asset_handle.AssetCategroy(request)
        data = categories.serialize_data()
	print HttpResponse(data)
        return HttpResponse(data)
    else:
        return render(request, 'assets/asset_category.html', {'category_type': category_type})


@login_required
def asset_event_logs(request, asset_id):
    if request.method == "GET":
        log_list = asset_handle.fetch_asset_event_logs(asset_id)
        return HttpResponse(json.dumps(log_list, default=utils.json_datetime_handler))


@login_required
def asset_detail(request, asset_id):
    if request.method == "GET":
        try:
            asset_obj = models.Asset.objects.get(id=asset_id)

        except ObjectDoesNotExist as e:
            return render(request, 'assets/asset_detail.html', {'error': e})
        return render(request, 'assets/asset_detail.html', {"asset_obj": asset_obj})


@login_required
def get_dashboard_data(request):
    '''返回主页面数据'''

    dashboard_data = AssetDashboard(request)
    dashboard_data.searilize_page()
    return HttpResponse(json.dumps(dashboard_data.data))
