from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^join/$', views.join, name='players-join'),
    url(r'^leave/(\d)$', views.leave, name='players-leave'),
    url(r'^maze/$', views.receive, name="players-receive"),
    url(r'^players', views.serve, name='players-serve')
]