from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
import json
from .utils import *

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
def bulk_upload(data):
    data = json.loads(data.body)
    message, status_code = start_stream(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
