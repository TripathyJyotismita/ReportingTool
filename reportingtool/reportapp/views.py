from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django import get_version
print(get_version)

from django.template import Template, Context
from django.http import HttpResponse
import datetime
import cx_Oracle

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
    query= """select ORDER_ID,CNAME from %s.dcsp_order where CNAME='ZCP' """ %(CONN_INFO['user'] )

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
    return render(request, 'reportapp/login.html')
#input_string={'uname':login.u_name}
#print(input_string)

def input_data(request):
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
        return HttpResponse("Enter the POP UP report template here")
