from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^bulk_upload/$', views.bulk_upload),
    re_path(r'^video_input/$', views.video_input)
]