from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
from assects.utils import *
import json
from common.utils import *



@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_assects(request):
    data = json.loads(request.body)
    response,status_code = add_assects_util(data)
    if status_code != 200:
        return HttpResponse( {message}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

        

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_assect(request):
    data = json.loads(request.body)
    response,status_code = update_assect_util(data)
    if status_code != 200:
        return HttpResponse( {message}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
