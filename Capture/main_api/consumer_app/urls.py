from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^consumer_video_input/$', views.consumer_video_input),
    re_path(r'^consumer_camera_preview/$', views.consumer_camera_preview),
    re_path(r'^consumer_camera_preview/(?P<wid>[A-Za-z0-9-_]+)/(?P<cameraname>[A-Za-z0-9-_.]+)/$', views.consumer_camera_preview)
]