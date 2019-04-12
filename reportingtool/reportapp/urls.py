from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    #url('', views.home, name='report-home'),
    url(r'login/$', views.login, name='login'),
    #url(r'report/$', views.process_request, name='report'),
    url(r'file', views.csv_view, name='file'),
    url(r'input_data/$', views.input_data, name='input_data'),

]