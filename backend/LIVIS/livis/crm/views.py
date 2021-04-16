from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
from .Leadsutils import *
from .Tasksutils import *
from .Todoutils import *
#from crm.utils import *
import json
from common.utils import *
from logs.utils import add_logs_util
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


def check_permission(request, perm_name):
    role = request.user.role_name
    mp = MongoHelper().getCollection("permissions")
    p = [i for i in mp.find()]
    if perm_name in p[0][role]:
        pass
    else:
        raise PermissionDenied


@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def update_lead(request):
    check_permission(request, "can_update_lead")
    data = json.loads(request.body)
    message, status_code = update_lead_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")


@api_view(['DELETE'])
@csrf_exempt
def delete_lead(request, id):
    check_permission(request, "can_delete_lead")
    message, status_code = delete_lead_util(id)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['POST'])
#@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def create_lead(request):
    check_permission(request, "can_create_lead")
    data = json.loads(request.body)
    message, status_code = create_lead_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_all_leads(request):
    check_permission(request, "can_get_all_leads")
    leads_list = get_all_leads_util()
    return HttpResponse(json.dumps( leads_list , cls=Encoder), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_single_lead(request, id):
    check_permission(request, "can_get_single_lead")
    leads_list = get_single_lead_util(id)
    return HttpResponse(json.dumps(leads_list , cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def check_gst(request, gst):
    check_permission(request, "can_check_gst")
    response = check_gst_util(gst)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['POST'])
#@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def create_task(request):
    check_permission(request, "can_create_task")
    data = json.loads(request.body)
    message, status_code = create_task_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_all_tasks(request, lead_id):
    check_permission(request, "can_get_all_tasks")
    tasks_list = get_all_tasks_util(lead_id)
    return HttpResponse(json.dumps( tasks_list , cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_single_task(request, id):
    check_permission(request, "can_get_single_task")
    tasks_list = get_single_task_util(id)
    return HttpResponse(json.dumps(tasks_list , cls=Encoder), content_type="application/json")

@api_view(['PATCH'])
#@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def update_task(request):
    check_permission(request, "can_update_task")
    data = json.loads(request.body)
    message, status_code = update_task_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['DELETE'])
#@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def delete_task(request, id):
    check_permission(request, "can_delete_task")
    message, status_code = delete_task_util(id)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['POST'])
#@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def create_todo(request):
    check_permission(request, "can_create_todo")
    data = json.loads(request.body)
    message, status_code = create_todo_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_all_todo(request, task_id):
    check_permission(request, "can_get_all_todo")
    print(task_id)
    leads_list = get_all_todo_util(task_id)
    return HttpResponse(json.dumps(leads_list , cls=Encoder), content_type="application/json")

@api_view(['PATCH'])
#@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def update_todo(request):
    check_permission(request, "can_update_todo")
    data = json.loads(request.body)
    message, status_code = update_todo_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['DELETE'])
#@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def delete_todo(request, task_id, todo_id):
    check_permission(request, "can_delete_todo")
    message, status_code = delete_todo_util(task_id, todo_id)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def update_lead_status(request):
    check_permission(request, "can_update_lead_status")
    data = json.loads(request.body)
    message, status_code = update_lead_status_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def create_lead_source(request):
    check_permission(request, "can_create_lead_source")
    data = json.loads(request.body)
    message, status_code = create_lead_source_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_all_lead_source(request):
    check_permission(request, "can_get_all_lead_source")
    leads_list = get_all_lead_source_util()
    return HttpResponse(json.dumps( leads_list , cls=Encoder), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_single_lead_source(request, id):
    check_permission(request, "can_get_single_lead_source")
    leads_list = get_single_lead_source_util(id)
    return HttpResponse(json.dumps(leads_list , cls=Encoder), content_type="application/json")

@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def delete_lead_source(request, id):
    check_permission(request, "can_delete_lead_source")
    message, status_code = delete_lead_source_util(id)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_users(request):
    response = get_users_util()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_tasks_by_user(request, user):
    response = get_tasks_by_user_util(user)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")