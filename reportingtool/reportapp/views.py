from django.shortcuts import render
from reportingtool import reportapp.reportapp.views
from reportingtool import reportapp as rt
from reportingtool  import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'templates/reportapp/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")