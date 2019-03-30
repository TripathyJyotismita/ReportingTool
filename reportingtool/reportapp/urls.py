from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    #url('', views.home, name='report-home'),
    url(r'login/$', views.login, name='report-login'),
]