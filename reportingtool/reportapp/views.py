from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
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

from django.http import StreamingHttpResponse

import datetime as dt

dtime = dt.datetime.now()
print(dtime)
print(dtime.tzinfo)

def pdf_view(result):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    fn = 'order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.pdf'
    return FileResponse(buffer, as_attachment=True, filename=fn)

def csv_view(result):
    print("view that streams a large CSV file.")
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    print("***********IN CSV_VIEW*******************88")
    print(result)
    for items in result:
        print(items)

    #rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    response=HttpResponse(content_type="text/csv")
    fn = 'order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.csv'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(fn)

    headers=['Date', 'CustomerName', 'No of Orders', 'Submitted Orders', 'Incomplete Orders']
    writer = csv.writer(response, delimiter=',')
    writer.writerow(i for i in headers)
    #writer.writerow(items for items in result)

    return response

def index(request):
    return render(request,'reportapp/index.html', {'content':['Homepage']})


def db_fun(c_name,from_date,to_date,report_format,for_date):
    CONN_INFO = {
        'host': '127.0.0.1',
        'port': 1521,
        'user': 'system',
        'psw': '0racleDB',
        'service': 'orcl.oradev.oraclecorp.com'
    }
    print(from_date+'************FROM DATE**************')
    print(to_date+'**************To Date***************')
    date_time_obj = datetime.datetime.strptime(from_date, "%Y-%m-%dT%H:%M")
    print('Date:', date_time_obj.date())
    print('Time:', date_time_obj.time())
    print('Date-time:', date_time_obj)
    to_date_obj= datetime.datetime.strptime(to_date, "%Y-%m-%dT%H:%M")
    print(to_date_obj)
    delta = to_date_obj-date_time_obj
    print(delta.days)
    #for_date_obj = datetime.datetime.strptime(for_date, "%Y-%m-%dT%H:%M")
    #print(for_date_obj)

    CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)
    query= """select * from %s.dcsp_order where CNAME='%s'""" % ((CONN_INFO['user']),c_name)
    #query = """select ORDER_ID,CNAME from {0}.dcsp_order where CNAME={1} """.format((CONN_INFO['user']),data['cn'])
    #query = "select * from SYSTEM.dcsp_order where 1=:CNAME "
    try:
        print("inside before db call"+c_name)
        #con = cx_Oracle.connect('system/0racleDB@127.0.0.1:1521/orcl.oradev.oraclecorp.com')
        con = cx_Oracle.connect(CONN_STR)
        # conn = cx_Oracle.connect(con)
        cur = con.cursor()
        print(con.version)
        print(query)
        cur.execute(query)
        #cur.execute(query, str(c_name))
        # cur.execute('select count(table_name) from ALL_TABLES')
        result = (cur.fetchall())
        cur.close()

        print(result)

    finally:
        con.close()

    print(report_format+"*******************************")

    if report_format == 'CSV':
        #print("roportformat is:" + report_format)
        #enerate_csv(result)
        csv_view(result)
    elif report_format == 'PDF':
        pdf_view(result)
    #elif report_format == 'EXCEL':
        #generate_excel(result)
#db_fun()

def home(request):
    now = datetime.datetime.now()
    t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    html = t.render(Context({'current_date': now}))
    return render(request,'reportapp/index.html')

@login_required
def login(request):
    if request.method == 'POST':
        print(request.method)
        print("**********Inside login post***********")
        #return HttpResponse('<h1>Welcome to Login page!!</h1>')
        u_name=request.POST.get("id_username")
        passwd=request.POST.get("id_password")
        #print(u_name)
        #print(passwd)
        user = authenticate(username=u_name, password=passwd)
        if user:
            if user.is_active:
                auth_login(request,user)
                messages.success(request, "You have logged in!")
                #return HttpResponse("You are logged in")
                #return redirect('reportapp/input_data.html')
                #return render_to_response('reportapp/input_data.html')
                # redirect_to = settings.LOGIN_REDIRECT_URL
                return render(request, 'reportapp/input_data.html', context={'username': u_name})
                # return HttpResponse("You are logged in")
                #return redirect('reportapp/input_data.html')
                # return render_to_response('reportapp/input_data.html')
            else:
                messages.warning("Your account is inactive!")
                return redirect('/login')

        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(u_name, passwd))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'reportapp/login_report.html')

def logout_view(request):
    #logout(request)
    return HttpResponse("Logout successfully!")

def input_data(request):
    c_name = request.POST.get("c_name")
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    for_date = request.POST.get("for_date")
    report_format = request.POST.get("report_format")
    print("IN INPUT_DATA-"+report_format)
    db_fun(c_name,from_date,to_date,report_format,for_date)
    #return HttpResponse("Report downloaded in your machine!")
    return render(request, 'reportapp/file_download.html')

