from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.template import RequestContext
from django import get_version
import csv,xlwt,xlsxwriter,sys
print(get_version)

from django.template import Template, Context
from django.http import HttpResponse
import datetime
import cx_Oracle
from fpdf import FPDF
from os import path
import os

def index(request):
    return render(request,'reportapp/index.html', {'content':['Homepage']})


def db_fun(c_name,from_date,to_date,report_format):
    print("inside DB fun******************************")
    CONN_INFO = {
        'host': '127.0.0.1',
        'port': 1521,
        'user': 'system',
        'psw': '0racleDB',
        'service': 'orcl.oradev.oraclecorp.com'
    }
    CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)
    query = """select * from %s.dcsp_order where CNAME='%s'""" % ((CONN_INFO['user']), c_name)
    #query= """select ORDER_ID,CNAME from %s.dcsp_order where CNAME=%s AND ORDER_ID='o10275' """ % ((CONN_INFO['user']),'ZCP')
    #query = """select ORDER_ID,CNAME from %s.dcsp_order where CNAME=%s AND ORDER_ID='o10275' """ % ((CONN_INFO['user']))
    #query= """select * from system.dcsp_order where CNAME=%s""" %(c_name)
    #query="""select * from {0}.dcsp_order where CNAME={1} """.format((CONN_INFO['user']),c_name)
    #print(c_name+'DBdun*****************')
    try:
        #con = cx_Oracle.connect('system/0racleDB@127.0.0.1:1521/orcl.oradev.oraclecorp.com')
        con = cx_Oracle.connect(CONN_STR)
        # conn = cx_Oracle.connect(con)
        cur = con.cursor()
        print(con.version)
        #print(report_format + 'inTRYYYYYYYYYYYYYYYY')
        print(query)
        cur.execute(query)
        # cur.execute('select count(table_name) from ALL_TABLES')
        result = (cur.fetchall())
        cur.close()

        print(result)
        if report_format == 'CSV':
            csv_view(result)
    finally:
        con.close()


#print(db_fun(c_name))






def home(request):
    now = datetime.datetime.now()
    t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
global uname

def login(request):
    print(request.method)
    print("**********Inside login post***********")
    #return HttpResponse('<h1>Welcome to Login page!!</h1>')
    u_name=request.POST.get("id_username")
    passwd=request.POST.get("id_password")
    #print(u_name)
    #print(passwd)
    return render(request, 'reportapp/input_data.html')

from io import BytesIO
def csv_view(result):
    bio = BytesIO()
    csv.writer(bio).writerow([unicode(r).encode('utf-8') for r in result])
    return bio.getvalue()

    import pdb
    print("view that streams a large CSV file.")
    print("***********IN CSV_VIEW*******************88")
    #print(result)

    #rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    response=HttpResponse(content_type="text/csv")
    fn = 'order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.csv'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(fn)

    with open(fn, 'a', newline='') as f:
        writer = csv.writer(response)
        #print(result)
        for i in result:
            print(i)
        writer.writerow(result)
        #writer = csv.writer(f)
        headers=('Date', 'CustomerName', 'No of Orders', 'Submitted Orders', 'Incomplete Orders')
        writer = csv.writer(response)
        #writer.writerow(['Date', 'CustomerName', 'No of Orders', 'Submitted Orders', 'Incomplete Orders'])
        writer.writerow(i for i in headers)
        #for row in data:
         #   writer.writerow(row)
        #pdb.set_trace()
        #writer.writelines(i for i in result
        #for items in result:
            #print(items)
            #writer.writerow(result)
          #  for j in items:
           #     writer.writerow(j)

        #for row in result:
           # writer.writerow(row)
    return response

def input_data(request):
        indata=False
        c_name = request.POST.get("c_name")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        tp = request.POST.get("tp")
        report_format = request.POST.get("report_format")
        print(report_format)
        #return HttpResponse("Enter the POP UP report template here1111111111")

        db_fun(c_name, from_date, to_date, report_format)
        return render(request, 'reportapp/file_download.html')

input_formats=['CSV Format','PDF Format']
