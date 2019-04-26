from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.platypus import Image, Paragraph, Table
from reportlab.lib import colors


from django.http import StreamingHttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
PAGESIZE = (140 * mm, 216 * mm)
BASE_MARGIN = 5 * mm
from io import BytesIO
pdf_buffer = BytesIO()
my_doc = SimpleDocTemplate(pdf_buffer)

class PdfCreator:
    def add_page_number(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "%d" % (doc.page)
        canvas.drawCentredString(
            0.75 * inch,
            0.75 * inch,
            page_number_text
        )
        canvas.restoreState()
    def get_body_style(self):
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['BodyText']
        body_style.fontSize = 18
        return body_style
    def build_pdf(self):
        pdf_buffer = BytesIO()
        my_doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=PAGESIZE,
            topMargin=BASE_MARGIN,leftMargin=BASE_MARGIN,rightMargin=BASE_MARGIN,
			bottomMargin=BASE_MARGIN)
        body_style = self.get_body_style()
        flowables = [Paragraph("First paragraph", body_style),Paragraph("Second paragraph", body_style)]
        my_doc.build(flowables,onFirstPage=self.add_page_number,onLaterPages=self.add_page_number,)
        pdf_value = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf_value

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



            #return '500'
    else:

        form = AuthenticationForm()
    return render(request, 'reportapp/login_report.html')

#def login(request):
 #   return render(request, 'reportapp/input_data.html')
def home(request):
    return render(request,'reportapp/homepage.html')

def input_data(request):
    c_name = request.POST.get("c_name")
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
        #messages.error(request, 'Enter transaction period/date')
        #return HttpResponseRedirect('reportapp/input_data.html')
        #return HttpResponse("Please select transaction period/date!")
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

        elif report_format =="PDF":
            from reportlab.platypus import LongTable, TableStyle, BaseDocTemplate, Frame, PageTemplate
            doc = BaseDocTemplate(
                "question.pdf",
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=50,
                bottomMargin=80,
                showBoundary=False)
            spacing = 2
            response = HttpResponse(content_type='application/pdf')
            fn1 = 'order_report ' + datetime.datetime.now().strftime("%Y-%m-%d") + '.pdf'
            response['Content-Disposition'] = 'attachment; filename={0}'.format(fn1)
            """data = [['00', '01', '02', '03', '04'],
                    ['10', '11', '12', '13', '14'],
                    ['20', '21', '22', '23', '24'],
                    ['30', '31', '32', '33', '34']]
            
            data = result
            k = []
            for i in data:
                k.append(list(i))
            for ele in k:
                print(type(ele))
                for c in ele:
                    print(type(c))
            print("k is", k)
            
            width = A4
            height = len(result)
            t = Table(data, 5, height)
            t.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)])
            print(t)
            """
            elements = []
            data = [['00', '01', '02', '03', '04'],
                    ['10', '11', '12', '13', '14'],
                    ['20', '21', '22', '23', '24'],
                    ['30', '31', '32', '33', '34']]
            t = Table(data)
            t.setStyle(TableStyle([('BACKGROUND', (1, 1), (-2, -2), colors.green),
                                   ('TEXTCOLOR', (0, 0), (1, -1), colors.red)]))
            elements.append(t)
            styles = getSampleStyleSheet()
            styleN = styles['Normal']
            frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')
            template = PageTemplate(id='longtable', frames=frame)
            doc.addPageTemplates([template])

            doc.build(elements)
            p = canvas.Canvas(response)
            p.setFont("Times-Roman", 55)
            p.drawString(100, 700, "Order report")
            #t.wrapOn(p, width, height)
            #t.drawOn(p, 0 * inch, 5 * inch)

            p.showPage()
            p.save()
            # return response
    finally:
        con.close()
    #messages.success(request, 'Report has been downloaded!')
    return response
    #return HttpResponse("Report downloaded in your machine!")
    #return render(request, 'reportapp/input_data.html')