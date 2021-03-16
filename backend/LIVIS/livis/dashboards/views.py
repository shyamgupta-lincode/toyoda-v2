from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
import json
from common.utils import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from bson.json_util import dumps
from bson.objectid import ObjectId
from dashboards.utils import *


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def total_production_by_wid(request):
    data = json.loads(request.body)
    response, status_code = total_production_by_wid_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def production_weekly(request):
    data = json.loads(request.body)
    response, status_code = production_weekly_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        print(response)
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def production_monthly(request):
    data = json.loads(request.body)
    response, status_code = production_monthly_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        print(response)
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def production_hourly(request):
    data = json.loads(request.body)
    response, status_code = production_hourly_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        print(response)
        return HttpResponse(json.dumps({'data':response} , cls=Encoder), content_type="application/json")


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def production_yield_by_wid(request):
    data = json.loads(request.body)
    response, status_code = production_yield_by_wid_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps( {'data': response}, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def production_rate(request):
    data = json.loads(request.body)
    response, status_code = production_rate_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps( {'data': response}, cls=Encoder), content_type="application/json")


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def defect_count(request):
    data = json.loads(request.body)
    response, status_code = defect_count_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps( {'data': response}, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def total_vs_planned(request):
    data = json.loads(request.body)
    response, status_code = total_vs_planned_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps( {'data': response}, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def defect_distribution(request):
    data = json.loads(request.body)
    response, status_code = defect_distribution_util(data)
    if status_code != 200:
        return HttpResponse({response}, status=status_code)
    else:
        return HttpResponse(json.dumps( {'data': response}, cls=Encoder), content_type="application/json")

