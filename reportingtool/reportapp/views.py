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
def dbConnection():
    print("Calling DBCONNECTION")
    CONN_INFO = {
        'host': 'localhost',
        'port': 1521,
        'user': 'system',
        'psw': '0racleDB',
        'service': 'orcl.oradev.oraclecorp.com'
    }
    CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)
    #con = cx_Oracle.connect('system/0racleDB@localhost:1521/orcl.oradev.oraclecorp.com')
    query = '''
             SELECT * from dual;
            '''
    try:
        conn = cx_Oracle.connect(CONN_STR)
        cursor = conn.cursor()
        result = cursor.execute(query).fetchall()
        print(result)

    finally:
        conn.close()

def home(request):
    now = datetime.datetime.now()
    t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)


def login(request):
    print(request.method)
    print("**********Inside login post***********")
    #return HttpResponse('<h1>Welcome to Login page!!</h1>')
    uname=request.POST.get("id_username")
    passwd=request.POST.get("id_password")
    print(uname)
    print(passwd)
    return render(request, 'reportapp/login.html')

def input_data(request):
    print ('**************')
    if request.method == "GET":
        print("*"*10)
        return render(request, "reportapp/input_data.html")
    elif request.method == "POST":
        #import pdb
        #pdb.set_trace()
        c_name= request.POST.get("c_name")
        print(c_name)
        return HttpResponse("Enter the POP UP report template here")
