from django import forms
from . import models as m
from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')
class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = m.UserProfileInfo
         #fields = m.UserProfileInfo.portfolio_site
         fields = ('portfolio_site', 'profile_pic')