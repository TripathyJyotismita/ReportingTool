from django.conf.urls import url
from . import views
# SET THE NAMESPACE!
app_name = 'reportapp'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'home', views.home, name='home'),
    url(r'^$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]