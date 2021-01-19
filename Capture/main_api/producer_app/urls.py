from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^producer_bulk_upload/$', views.producer_bulk_upload),
    re_path(r'^producer_video_input/$', views.producer_video_input)
]