from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url('home/$', views.home, name='home'),
    url(r'login/$', views.login, name='login'),
    #url(r'login/$', views.login, name='login'),
    #url(r'logout/$',views.logout_view, name='logout'),
    #url(r'report/$', views.process_request, name='report'),
    url(r'file_download/$', views.csv_view, name='file_download'),
    #url(r'file_download/$', views.pdf_view, name='file_download'),
    url(r'input_data/$', views.input_data, name='input_data'),

]