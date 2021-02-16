from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
from inspection.utils import *
import json
from common.utils import *

from logs.utils import add_logs_util

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def plan_production_counter_modify(request):
    data = json.loads(request.body)
    from inspection.utils import plan_production_counter_modify_util
    response = plan_production_counter_modify_util(data)
    return HttpResponse(json.dumps(response,cls=Encoder), content_type="application/json")
    
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_running_process(request,workstation_id):
    #print("viewssss")
    response,status_code = get_running_process_util(workstation_id)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
    
    
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_metrics(request,inspection_id):
    
    response,status_code = get_metrics_util(inspection_id)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")    
        
        
        
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_virtual_button(request):
    data = json.loads(request.body)
    print("virtual button :::::::::::::::::::::")
    print(data)
    from inspection.utils import get_virtual_button_util
    resp = get_virtual_button_util(data)
    return HttpResponse(json.dumps( {'message' : resp} , cls=Encoder), content_type="application/json")
    #part_id = data.get('part_id')
    # print(part_id)
    # if part_id:
    #     resp = get_feature_util(part_id)
    #     return HttpResponse(json.dumps( resp , cls=Encoder), content_type="application/json")
    # return HttpResponse(json.dumps( {'message' : "Failed"} , cls=Encoder), content_type="application/json")
    

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def start_process(request):
    token_user_id = request.user.user_id
    operation_type = "inspection"
    notes = "start inspection"
    
    add_logs_util(token_user_id,operation_type,notes)
    
    
    data = json.loads(request.body)
    
    
    response,status_code = start_process_util(data,token_user_id)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def end_process(request):
    token_user_id = request.user.user_id
    operation_type = "inspection"
    notes = "start inspection"
    
    add_logs_util(token_user_id,operation_type,notes)
    
    
    data = json.loads(request.body)
    
    
    response,status_code = end_process_util(data,token_user_id)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
        

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def report_process(request):
    token_user_id = request.user.user_id
    operation_type = "inspection"
    notes = "start inspection"
    
    add_logs_util(token_user_id,operation_type,notes)
    
    
    data = json.loads(request.body)
    
    
    response,status_code = report_process_util(data,token_user_id)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

