from django.shortcuts import render
from django.template import loader

from django import get_version
print(get_version)

from django.template import Template, Context
from django.http import HttpResponse
import datetime
import cx_Oracle

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

def hello(request):
    return HttpResponse('<h1>hello!!</h1>')

def login(request):
    #return HttpResponse('<h1>Welcome to Login page!!</h1>')
    return render(request, 'reportapp/login.html')

def process_request(request):
    return render(request, "reportapp/rselection.html")