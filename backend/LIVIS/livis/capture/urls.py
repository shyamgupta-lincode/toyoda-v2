from django.urls import path, re_path

from capture import views

urlpatterns = [


    re_path(r'^capture_image/$', views.capture_image),
    re_path(r'^get_capture_feed_url/$', views.get_capture_feed_url),
    re_path(r'^get_inference_feed_url/(?P<wsid>[A-Za-z0-9-_]+)/(?P<partid>[A-Za-z0-9-_.]+)/$',
            views.get_inference_feed_url),
    re_path(r'^camera_selection/$', views.camera_selection),
    re_path(r'^consumer_camera_preview/(?P<wid>[A-Za-z0-9-_]+)/(?P<cameraname>[A-Za-z0-9-_.]+)/$',
            views.consumer_camera_preview),
    re_path(r'^inference_camera_preview/(?P<wid>[A-Za-z0-9-_]+)/(?P<cameraname>[A-Za-z0-9-_.]+)/'
            r'(?P<partid>[A-Za-z0-9-_.]+)/$', views.inference_feed),
    re_path(r'^camera_select_preview/(?P<ws_location>[A-Za-z0-9-_]+)/(?P<cameraid>[A-Za-z0-9-_.]+)/$',
            views.camera_select_preview),
    re_path(r'^get_camera_select_url/(?P<ws_location>[A-Za-z0-9-_]+)/$',
            views.get_camera_select_url)
]
