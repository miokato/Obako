from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='obako top'),
    url(r'^callback', views.callback, name='obako'),
]