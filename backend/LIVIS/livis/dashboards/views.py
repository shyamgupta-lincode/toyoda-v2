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

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def total_production(request):
    data = total_production_util()
    return HttpResponse(json.dumps(data , cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def production_yield(request):
    data = production_yield_util()
    return HttpResponse(json.dumps( data , cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def defect_count(request):
    data = defect_count_util()
    return HttpResponse(json.dumps( data , cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def total_vs_planned(request):
    data = total_vs_planned_util()
    return HttpResponse(json.dumps( data , cls=Encoder), content_type="application/json")
