from django.urls import path,re_path
from crm import views

urlpatterns = [
    re_path(r'^update_lead/$', views.update_lead),
    re_path(r'^get_all_leads/$', views.get_all_leads),
    re_path(r'^get_single_lead/(?P<id>[A-Za-z0-9-_]+)/$', views.get_single_lead),
    re_path(r'^create_lead/$', views.create_lead),
    re_path(r'^delete_lead/(?P<id>[A-Za-z0-9-_]+)/$', views.delete_lead),
    re_path(r'^check_gst/(?P<gst>[A-Za-z0-9-_]+)/$', views.check_gst),
    re_path(r'^update_task/$', views.update_task),
    re_path(r'^get_all_tasks/$', views.get_all_tasks),
    re_path(r'^get_single_task/(?P<id>[A-Za-z0-9-_]+)/$', views.get_single_task),
    re_path(r'^create_task/$', views.create_task),
    re_path(r'^delete_task/(?P<id>[A-Za-z0-9-_]+)/$', views.delete_task)
]
