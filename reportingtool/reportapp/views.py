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


def db_fun():
    CONN_INFO = {
        'host': '127.0.0.1',
        'port': 1521,
        'user': 'system',
        'psw': '0racleDB',
        'service': 'orcl.oradev.oraclecorp.com'
    }
    CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)
    c_name='null'
    #query= """select ORDER_ID,CNAME from %s.dcsp_order where CNAME=%s AND ORDER_ID='o10275' """ % ((CONN_INFO['user']),'ZCP')
    query = """select ORDER_ID,CNAME from %s.dcsp_order where CNAME='ZCP' AND ORDER_ID='o10275' """ % ((CONN_INFO['user']))
    try:
        #con = cx_Oracle.connect('system/0racleDB@127.0.0.1:1521/orcl.oradev.oraclecorp.com')
        con = cx_Oracle.connect(CONN_STR)
        # conn = cx_Oracle.connect(con)
        cur = con.cursor()
        print(con.version)
        cur.execute(query)
        # cur.execute('select count(table_name) from ALL_TABLES')
        result = (cur.fetchall())
        cur.close()

        return result
    finally:
        con.close()
print(db_fun())

def generate_pdf():
    spacing=2
    title = 'Order Report for Customers'
    pdf = FPDF(format='letter', unit='in')
    pdf.add_page()
    pdf.set_font('Arial', '', 10.0)

    epw = pdf.w - 4 * pdf.l_margin
    col_width = epw / 5
    data = [['Date', 'Customer Name', 'No of Orders', 'Submitted Orders', 'Incomplete Orders'],
            ['04-08-19', 'ZCP', '57', '15', '35'],
            ['04-08-19', 'ZCP', '59', '32', '23'],
            ['04-08-19', 'ZCP', '88', '28', '21']
            ]

    pdf.set_font('Arial', 'B', 14.0)
    # pdf.cell(w, h = 0, txt = '', border = 0, ln = 0, align = '', fill = False, link = '')
    pdf.cell(epw, 1.0, 'Order Report', align='C')
    pdf.set_font('Arial', '', 10.0)
    pdf.ln(1)
    row_h = pdf.font_size
    th=row_h*spacing
    for row in data:
        print(row)
        for datum in row:
            print(datum)
            pdf.cell(col_width, th, str(datum), border=1, align='C')
        pdf.ln(th)

    # pdf.ln(5*th)

    pdf.output('order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.pdf', 'F')
#generate_pdf()

def generate_csv():
    #handle = open(sys.argv[1])
    data = [['Date', 'Customer Name', 'No of Orders', 'Submitted Orders', 'Incomplete Orders'],
            ['04-08-19', 'ZCP', '57', '15', '35'],
            ['04-08-19', 'ZCP', '59', '32', '23'],
            ['04-08-19', 'ZCP', '88', '28', '21']
            ]
    with open(('order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.csv'), 'w') as fp:
        writer=csv.writer(fp,delimiter=',')
        writer.writerow(['Date', 'Customer Name', 'No of Orders', 'Submitted Orders', 'Incomplete Orders'])
        for row in data:
            writer.writerow(row)

#generate_csv()

def generate_excel():
    wb=xlsxwriter.Workbook('order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.xlsx')
    ws=wb.add_worksheet()
    row = 0
    column =0
    data = (['Date', 'Customer Name', 'No of Orders', 'Submitted Orders', 'Incomplete Orders'],
            ['04-08-19', 'ZCP', '57', '15', '35'],
            ['04-08-19', 'ZCP', '59', '32', '23'],
            ['04-08-19', 'ZCP', '88', '28', '21']
            )
    for date,cname,no,so,io in data:
        #ws.write(row,column,item)
        ws.write(row, column,date)
        ws.write(row, column+1,cname)
        ws.write(row, column + 2, no)
        ws.write(row, column + 3, so)
        ws.write(row, column + 4, io)
        row+=1
    wb.close()
#generate_excel()






def home(request):
    now = datetime.datetime.now()
    t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
global uname

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
#input_string={'uname':login.u_name}
#print(input_string)

def input_data(request):
    indata=False
    c_name = request.POST.get("c_name")
    from_date = request.POST.get("from_date")
    print(from_date)
    to_date = request.POST.get("to_date")
    print(to_date)
    tp = request.POST.get("tp")
    print(tp)
    report_format = request.POST.get("report_format")
    print(report_format)
    return HttpResponse("Enter the POP UP report template here1111111111")


def input_data1(request):
        print('******Inside input_data GET method********')
        if request.method == "GET":
            print("*"*10)
            return render(request, "reportapp/input_data.html")
            #return render(request, "reportapp/rselection.html")
        elif request.method == "POST":
            input_string=""
            #import pdb
            #pdb.set_trace()
            c_name = request.POST.get("c_name")
            print(c_name)
            from_date = request.POST.get("from_date")
            print(from_date)
            to_date = request.POST.get("to_date")
            print(to_date)
            tp = request.POST.get("tp")
            print(tp)
            report_format = request.POST.get("report_format")
            print(report_format)
            return HttpResponse("Enter the POP UP report template here")
