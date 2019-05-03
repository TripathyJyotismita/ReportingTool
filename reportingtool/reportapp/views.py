from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django import get_version
import csv,xlwt,xlsxwriter,sys
print(get_version)

from django.template import Template, Context, loader, RequestContext
from django.http import HttpResponse
import datetime
import cx_Oracle
from fpdf import FPDF
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from os import path
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.platypus import Image, Paragraph, Table
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch

def home(request):
    return render(request,'reportapp/homepage.html')

def logout(request):
    auth_logout(request)
    return render(request,"reportapp/logout.html");

def login(request):
    if request.method == 'POST':
        print("INSIDE LOGIN FUN********************")
        form = AuthenticationForm(request.POST)
        u_name=request.POST.get("id_username")
        print(u_name)
        passwd=request.POST.get("id_password")
        user = authenticate(username=u_name, password=passwd)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                messages.success(request, "You have logged in!")
                return render(request, 'reportapp/input_data.html', context={'username': u_name})
                # return HttpResponse("You are logged in")
                # return render_to_response('reportapp/input_data.html')
            else:
                messages.error(request,'username or password not correct')
                return redirect('/login')

        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(u_name, passwd))
            #return HttpResponse("Invalid login details given")
            #return redirect('/login')
            if HttpResponse.status_code == 500:
                messages.error(request, "You wrong logged !")

    else:

        form = AuthenticationForm()
    return render(request, 'reportapp/login_report.html')

def input_data(request):
    print("INSIDE INPUT_DATA FUN********************")
    c_name = request.POST.get("Selector")
    print(c_name)
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    for_date = request.POST.get("for_date")
    print(for_date)
    report_format = request.POST.get("report_format")
    print(report_format)
    display_type = request.POST.get("display_type", None)
    return HttpResponse("CNAME HAS BEEN SELECTED!")

    '''if 'Transaction' in request.POST:
        print("Transaction has been selected!!!!!!!!!!!!!!!!!")
        return HttpResponse("THRANSACTION P HAS BEEN SELECTED!")
        #return db_fun(request,c_name,from_date,to_date,report_format)
    else:
        print("TransactionDate is selected!!!!!!!!!!!!!!!!!!!!")
        return render(request, 'reportapp/transaction_error_page.html')'''