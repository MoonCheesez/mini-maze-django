from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^controller/player([1-4])$', views.player_control, name='player_control-player_control'),
]