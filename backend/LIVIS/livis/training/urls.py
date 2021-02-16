from django.urls import path,re_path
from django.conf.urls import url
from training import views

urlpatterns = [

               url(r'^deploy_experiment/$', views.deploy_experiment),
               url(r'^set_threshold/$', views.set_threshold),
               url(r'^create_experiment/$', views.create_experiment_modified),
               url(r'^create_retrain_experiment/$', views.create_retrain_experiment),
               url(r'^get_model_data/(?P<experiment_type>[A-Za-z0-9-_]+)$', views.get_model_data),
               url(r'^get_deployment_list/$', views.get_deployment_list),
               url(r'^get_all_running_experiments/$', views.get_all_running_experiments), 
               #url(r'^get_running_experiment/(?P<part_id>[A-Za-z0-9-_]+)$', views.get_running_experiment), 
               url(r'^experiment_status/(?P<part_id>[A-Za-z0-9-_]+)/(?P<experiment_id>[A-Za-z0-9-_]+)$', views.get_experiment_status),
               
               #url(r'^deploy_experiment/$', views.deploy_experiment)

]
