from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
import json
from .utils import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.http import HttpResponse,StreamingHttpResponse


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_capture_feed_url(request):
    from capture.utils import get_camera_feed_urls
    url = get_camera_feed_urls()
    return HttpResponse(json.dumps({'data': url}), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_inference_feed_url(request, wsid, partid):
    from capture.utils import get_inference_feed_url_util
    url = get_inference_feed_url_util(wsid , partid)
    return HttpResponse(json.dumps({'data': url}), content_type="application/json")
    
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def capture_image(request):
    data = json.loads(request.body)
    message, status_code = capture_image_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def consumer_camera_preview(request,wid,cameraname):
    return StreamingHttpResponse(start_camera_preview(wid,cameraname), content_type='multipart/x-mixed-replace; boundary=frame')

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def inference_feed(request,wid,cameraname,partid):
    return StreamingHttpResponse(start_inference(wid,cameraname,partid), content_type='multipart/x-mixed-replace; boundary=frame')

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def camera_selection(data):
    data = json.loads(data.body)
    print(data)
    message, status_code = start_camera_selection(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def camera_select_preview(request, ws_location, cameraid):
    return StreamingHttpResponse(get_camera_index_util(ws_location, cameraid),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_camera_select_url(request, ws_location):
    url = get_camera_select_url_util(ws_location)
    return HttpResponse(json.dumps({'data': url}), content_type="application/json")

