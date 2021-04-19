from django.urls import path, re_path
from train_kpis import views

urlpatterns = [
    re_path(r'^loss_vs_epoch/$', views.loss_vs_epoch),
    re_path(r'^reg_loss_vs_epoch/$', views.reg_loss_vs_epoch),
    re_path(r'^class_loss_vs_epoch/$', views.class_loss_vs_epoch),
    re_path(r'^map_vs_epoch/$', views.map_vs_epoch),
    re_path(r'^lr_vs_epoch/$', views.lr_vs_epoch),
    re_path(r'^retinanet_training_stats/$', views.retinanet_training_stats),
    re_path(r'^retinanet_epoch_status/$', views.retinanet_epoch_status)
]

