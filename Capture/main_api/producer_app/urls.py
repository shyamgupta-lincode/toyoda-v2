from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^producer_bulk_upload/$', views.producer_bulk_upload),
    re_path(r'^producer_video_input/$', views.producer_video_input),
    re_path(r'^producer_camera_selection/$', views.producer_camera_selection),
    re_path(r'^producer_camera_preview/(?P<wid>[A-Za-z0-9-_]+)/(?P<cameraname>[A-Za-z0-9-_.]+)/$', views.producer_camera_preview)
]