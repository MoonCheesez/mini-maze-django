from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^controller/$', views.player_control, name='player_control-player_control'),
]