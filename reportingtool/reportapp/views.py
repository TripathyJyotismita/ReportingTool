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

def login(request):
    return render(request, 'reportapp/input_data.html')

def input_data(request):
    c_name = request.POST.get("c_name")
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    for_date = request.POST.get("for_date")
    report_format = request.POST.get("report_format")

    CONN_INFO = {
        'host': '127.0.0.1',
        'port': 1521,
        'user': 'system',
        'psw': '0racleDB',
        'service': 'orcl.oradev.oraclecorp.com'
    }

    CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)
    query = """select * from %s.dcsp_order where CNAME='%s'""" % ((CONN_INFO['user']), c_name)
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
                headers = ['Date', 'CustomerName', 'No of Orders', 'Submitted Orders', 'Incomplete Orders']
                writer = csv.writer(response, delimiter=',')
                writer.writerow(headers)
                for row in result:
                    writer.writerow(row)
            response['Content-Disposition'] = 'attachment; filename={0}'.format(fn)
        elif report_format =="PDF":
            print(report_format)
            print("THIS IS INSIDE PDF @@@@@@@@@@@@@@@")
            response = HttpResponse(content_type="application/pdf")
            spacing = 2
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
            pdf.ln(5)
            row_h = pdf.font_size
            print(row_h)
            th = row_h * spacing
            print(th)
            for row in result:
                print(row)
                for datum in row:
                    print(str(datum))
                    print(col_width)
                    pdf.cell(col_width, th, str(datum), border=1, align='C')
                pdf.ln(th)
                print(pdf.ln(th))

            # pdf.ln(5*th)
            fn1 = 'order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.pdf'
            pdf.output(fn1, 'F')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(fn1)
    finally:
        con.close()

    return response
    #return HttpResponse("Report downloaded in your machine!")
    #return render(request, 'reportapp/input_data.html')