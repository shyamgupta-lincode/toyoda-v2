from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
import json
from common.utils import *
from common.utils import Encoder
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from bson.json_util import dumps
from bson.objectid import ObjectId
from train_kpis.utils import *


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def loss_vs_epoch(request):
    data = json.loads(request.body)
    response, status_code = loss_vs_epoch_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def reg_loss_vs_epoch(request):
    data = json.loads(request.body)
    response, status_code = reg_loss_vs_epoch_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def class_loss_vs_epoch(request):
    data = json.loads(request.body)
    response, status_code = class_loss_vs_epoch_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def map_vs_epoch(request):
    data = json.loads(request.body)
    response, status_code = map_vs_epoch_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def lr_vs_epoch(request):
    data = json.loads(request.body)
    response, status_code = lr_vs_epoch_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def retinanet_training_stats(request):
    data_json = json.loads(request.body)
    from train_kpis.utils import retinanet_training_stats_utils
    response, status_code = retinanet_training_stats_utils(data_json)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response , cls=Encoder), content_type="application/json")



@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def retinanet_epoch_status(request):
    data_json = json.loads(request.body)
    from train_kpis.utils import retinanet_epoch_status_utils
    response, status_code = retinanet_epoch_status_utils(data_json)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response , cls=Encoder), content_type="application/json")   

# @api_view(['POST'])
# @csrf_exempt
# def retinanet_training_stats(request):
#     config = json.loads(request.body)
#     from train_kpis.utils import retinanet_training_stats_utils
#     response= retinanet_training_stats_utils(config)
#     # response = json.loads(response)
#     # experiment_id_ = str(experiment_id_)
#     # response = {'data': response}
#     return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")    

