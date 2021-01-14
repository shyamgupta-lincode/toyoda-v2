from django.urls import path,re_path
from logs import views


urlpatterns = [
    # re_path(r'^testLogs/$', views.test_logs),
    re_path(r'^addLogs/$', views.add_logs),
    re_path(r'^getAaccessLog/$', views.get_access_log_report),
    re_path(r'^export_logs/$', views.export_logs),


]
