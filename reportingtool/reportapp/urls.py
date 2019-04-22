from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'login/$', views.login, name='login'),
    url(r'input_data/$', views.input_data, name='input_data'),

]