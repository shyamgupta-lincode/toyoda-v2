import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from common.utils import Encoder
from pathlib import Path
from common.utils import MongoHelper
from training.tasks import process_job_request

from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema

@api_view(['GET'])
@csrf_exempt
def get_model_data(request,experiment_type):
    #config = json.loads(request.body)
    from training.tasks import get_model,create_model_collections
    # client =MongoClient('localhost', 27017)
    # mp = client.Model_Collection
    # para = mp.model_collection.find({"model_type":config["model_type"]})
    create_collection = create_model_collections()
    para = get_model(experiment_type)
    
    # print(para)
    return HttpResponse(json.dumps(para, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
def set_threshold(request):
    config = json.loads(request.body)
    from training.tasks import set_threshold_util
    message= set_threshold_util(config)
    return HttpResponse(json.dumps(message, cls=Encoder), content_type="application/json")
    
    
@api_view(['POST'])
@csrf_exempt
def create_experiment_modified(request):
    config = json.loads(request.body)
    from training.tasks import add_experiment_modified
    experiment_id_= add_experiment_modified(config)
    experiment_id_ = str(experiment_id_)
    response = {'experiment_id': experiment_id_}
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
def create_retrain_experiment(request):
    config = json.loads(request.body)
    from training.tasks import add_retrain_experiment
    status = add_retrain_experiment(config)
    response = {"status":status}
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")



@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'experiment_name' : openapi.Schema(type=openapi.TYPE_STRING, example='test_tf_1'),
        'part_id': openapi.Schema(type=openapi.TYPE_STRING, example='5f42b5a90b72e674c03691d5'),
        'selected_labels' : openapi.Schema(type=openapi.TYPE_STRING, example='["Classification", "Hole", "hole1"]'),
        'type' : openapi.Schema(type=openapi.TYPE_STRING, example='tf'),
    }
))




@api_view(['POST'])
@csrf_exempt
def create_experiment(request):
    config = json.loads(request.body)
    from training.tasks import process_job_request, add_experiment
    experiment_id = add_experiment(config)
    experiment_id = str(experiment_id)
    process_job_request.delay(config, experiment_id)
    response = {'experiment_id': experiment_id}
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")



@api_view(['GET'])
@csrf_exempt
def get_experiment_status(request,part_id, experiment_id):
    from training.tasks import get_experiment_status
    response = get_experiment_status(part_id, experiment_id)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
def get_running_experiment(request,part_id):
    from training.tasks import get_running_experiment_status
    response = get_running_experiment_status(part_id)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
def get_all_running_experiments(request):
    from training.tasks import get_all_running_experiments_status
    response = get_all_running_experiments_status()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
def deploy_experiment(request):
    deployment_task = json.loads(request.body)
    from training.tasks import deploy_experiment_util
    deployment_status = deploy_experiment_util(deployment_task)
    return HttpResponse(json.dumps({'status' : 'Success!', 'deployment_status' : deployment_status}, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
def get_deployment_list(request):
    from training.tasks import get_deployment_list_util
    response = get_deployment_list_util()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
