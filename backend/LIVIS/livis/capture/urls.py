from django.urls import path, re_path

from capture import views

urlpatterns = [


    re_path(r'^consumer_video_input/(?P<wid>[A-Za-z0-9-_]+)/(?P<partid>[A-Za-z0-9-_.]+)/'
            r'(?P<cameraname>[A-Za-z0-9-_.]+)/$', views.consumer_video_input),
    re_path(r'^get_capture_feed_url/$', views.get_capture_feed_url),
            

    re_path(r'^consumer_camera_preview/(?P<wid>[A-Za-z0-9-_]+)/(?P<cameraname>[A-Za-z0-9-_.]+)/$', views.consumer_camera_preview)
]
