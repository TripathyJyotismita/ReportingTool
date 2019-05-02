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

import json


json_file='''
{"CLIENTDETAILS": [
{
	"TENANT_ID": "pz2ea0c0",
    "CLIENT_NAME": "India Test",
    "DB_NODES": ["vmatgz2ea006","vmatgz2ea007"],
    "ADMIN_NODES": "vmatgz2ea001",
    "AUX_NODES": ["vmatgz2ea002","vmatgz2ea003"],
    "STORE_NODES": ["vmatgz2ea002","vmatgz2ea003"],
    "OBIEE_NODE": "vmatgz2ea001",
    "SSE_NODES": ["vmatgz2ea010","vmatgz2ea011"],
    "ENDECA_NODES": ["vmatgz2ea001","vmatgz2ea004","vmatgz2ea005"],
    "LIVE": "NO",
    "TIER": "SMALL"}]
}
'''
#data=json.loads(json_file)
#print(data)
fp="C:\\Users\\jytripat\\Desktop\\ReportingTool\\reportingtool\\Sample-json-file.json"
with open (fp, 'r') as f:
	parsed_json = json.load(f)
print(parsed_json)
c_name='ZCP'


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        u_name=request.POST.get("id_username")
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

def logout(request):
    auth_logout(request)
    return render(request,"reportapp/logout.html");
def home(request):
    return render(request,'reportapp/homepage.html')

def input_data(request):
    c_name = request.POST.get("c_name")
    print(c_name)
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    for_date = request.POST.get("for_date")
    report_format = request.POST.get("report_format")
    display_type = request.POST.get("display_type", None)

    if 'Transaction' in request.POST:
        print("Transaction has been selected!!!!!!!!!!!!!!!!!")
        #return HttpResponse("THRANSACTION P HAS BEEN SELECTED!")
        return db_fun(request,c_name,from_date,to_date,report_format)
    else:
        print("TransactionDate is selected!!!!!!!!!!!!!!!!!!!!")
        return render(request, 'reportapp/transaction_error_page.html')

def db_fun(request,c_name,from_date,to_date,report_format):
    CONN_INFO = {
        'host': '127.0.0.1',
        'port': 1521,
        'user': 'system',
        'psw': '0racleDB',
        'service': 'orcl.oradev.oraclecorp.com'
    }

    CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)
    query = """select * from %s.dcsp_order where CNAME='%s' """ % ((CONN_INFO['user']), c_name)
    try:
        con = cx_Oracle.connect(CONN_STR)
        cur = con.cursor()
        print(con.version)
        print(query)
        cur.execute(query)
        # cur.execute(query, str(c_name))
        # cur.execute('select count(table_name) from ALL_TABLES')
        result = (cur.fetchall())
        #cur.close()
        print("result: ", result)
        if report_format == "CSV":
            #print(report_format)
            print("THIS IS INSIDE CSV @@@@@@@@@@@@@@@")
            response = HttpResponse(content_type="text/csv")
            fn = 'order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.csv'
            with open(fn, 'w', newline='') as f:
                #writer = csv.writer(f)
                headers = ['ORDER-ID', 'STATE', 'CREATED-DATE', 'SUBMITTED-DATE', 'CUSTOMER-NAME']
                writer = csv.writer(response, delimiter=',')
                writer.writerow(headers)
                for row in result:
                    writer.writerow(row)
            response['Content-Disposition'] = 'attachment; filename={0}'.format(fn)
        elif report_format == "EXCEL":
            #print(report_format)
            print("THIS IS INSIDE EXCEL @@@@@@@@@@@@@@@")
            response = HttpResponse(content_type="text/csv")
            fn = 'order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.xls'
            with open(fn, 'w', newline='') as f:
                #writer = csv.writer(f)
                headers = ['ORDER-ID', 'STATE', 'CREATED-DATE', 'SUBMITTED-DATE', 'CUSTOMER-NAME']
                writer = csv.writer(response, delimiter=',')
                writer.writerow(headers)
                for row in result:
                    writer.writerow(row)
            response['Content-Disposition'] = 'attachment; filename={0}'.format(fn)
        elif report_format == "TXT":
            # print(report_format)
            print("THIS IS INSIDE EXCEL @@@@@@@@@@@@@@@")
            response = HttpResponse(content_type="text/txt")
            fn = 'order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.txt'
            with open(fn, 'w', newline='') as f:
                # writer = csv.writer(f)
                headers = ['ORDER-ID', 'STATE', 'CREATED-DATE', 'SUBMITTED-DATE', 'CUSTOMER-NAME']
                writer = csv.writer(response, delimiter=',')
                writer.writerow(headers)
                for row in result:
                    writer.writerow(row)
            response['Content-Disposition'] = 'attachment; filename={0}'.format(fn)

    finally:
        con.close()
    #messages.success(request, 'Report has been downloaded!')
    return response
    #return HttpResponse("Report downloaded in your machine!")
    #return render(request, 'reportapp/input_data.html')