from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
from crm.utils import *
import json
from common.utils import *
from logs.utils import add_logs_util
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def update_lead(request):
    data = json.loads(request.body)
    message, status_code = update_lead_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def delete_lead(request, id):
    message, status_code = delete_lead_util(id)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def create_lead(request):
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
    leads_list = get_all_leads_util()
    return HttpResponse(json.dumps( leads_list , cls=Encoder), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_single_lead(request, id):
    leads_list = get_single_lead_util(id)
    return HttpResponse(json.dumps(leads_list , cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def check_gst(request, gst):
    response = check_gst_util(gst)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def create_task(request):
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
    tasks_list = get_all_tasks_util(lead_id)
    return HttpResponse(json.dumps( tasks_list , cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_single_task(request, id):
    tasks_list = get_single_task_util(id)
    return HttpResponse(json.dumps(tasks_list , cls=Encoder), content_type="application/json")

@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def update_task(request):
    data = json.loads(request.body)
    message, status_code = update_task_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def delete_task(request, id):
    message, status_code = delete_task_util(id)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def create_todo(request):
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
    print(task_id)
    leads_list = get_all_todo_util(task_id)
    return HttpResponse(json.dumps(leads_list , cls=Encoder), content_type="application/json")

@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def update_todo(request):
    data = json.loads(request.body)
    message, status_code = update_todo_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")

@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@permission_classes((AllowAny,))
def delete_todo(request, task_id, todo_id):
    message, status_code = delete_todo_util(task_id, todo_id)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")
