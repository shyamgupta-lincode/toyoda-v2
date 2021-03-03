from django.urls import path, re_path
from dashboards import views

urlpatterns = [
    re_path(r'^total_production/$', views.total_production),
    re_path(r'^production_yield/$', views.production_yield),
    re_path(r'^defect_count/$', views.defect_count),
    re_path(r'^total_vs_planned/$', views.total_vs_planned)
]
