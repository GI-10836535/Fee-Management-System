from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from superuser.models import AssignPaymentDuration, FeeType, FeeDescription, Invoice, InvoiceDetails
from .models import *
from datetime import datetime, timedelta

# PDF stuff
from django.template.loader import get_template
from xhtml2pdf import pisa

import io
from django.http import FileResponse


member = 'Gideon K. Impraim'
# member = 'Samuel Ofosu'

# Create your views here.

def invoice_details_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    company = InvoiceDetails.objects.get(pk=1)
    detail = get_object_or_404(Payments, pk=pk)
    # items = get_object_or_404(FeeItems, pk=pk)

    # temp_invoice = [int(invoice.total_amount) for invoice in Invoice.objects.all()]
    invoice = Invoice.objects.get(fee_type= detail.fee_type, branch= detail.branch, member_category= detail.member_category, group= detail.group, subgroup= detail.subgroup)

    keys = [item.fee_items for item in invoice.fee_items.all()]
    values = [int(i) for i in invoice.items_amount.split(',')]
    data = dict(zip(keys, values))

    template_path = 'client/user_printer.html'
    context = {
        'detail': detail,
        'company': company, 
        'invoice': invoice,
        'data': data
         }


    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')


    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response )

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




def index(request):
    template_name = 'client/index.html'
    total_invoice = 0
    total_payments = 0
    total_arrears = 0


    temp_invoice = [int(invoice.total_invoice) for invoice in AssignPaymentDuration.objects.all().filter(member=member)]
    temp_payments = [int(payment.amount_paid) for payment in Payments.objects.all().filter(member=member)]
    temp_arrears = [int(payment.arrears) for payment in Payments.objects.all().filter(member=member)]

    for i in temp_invoice:
        total_invoice += i

    for i in temp_payments:
        total_payments += i

    for i in temp_arrears:
        total_arrears += i  

    return render(request, template_name, {
        'total_invoice': total_invoice,
        'total_payments': total_payments,
        'total_arrears': total_arrears,
    })



def viewAssignedPayments(request):
    template_name = 'client/view-assigned-payments.html'
    assigned = AssignPaymentDuration.objects.all().filter(member=member).order_by('-id')
    user = AssignPaymentDuration.objects.all().filter(member=member).first()
    
    return render(request, template_name,{
        'assigned': assigned,
        'user': user,
    })




def makePayments(request, **kwargs):
    template_name = 'client/make-payment.html'
    pk = kwargs.get('pk')
    assigned = get_object_or_404(AssignPaymentDuration, pk=pk)
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day


    if request.method == 'POST':
        branch = request.POST.get('branch')
        member_category = request.POST.get('member_category')
        group = request.POST.get('group')
        subgroup = request.POST.get('subgroup')
        member = request.POST.get('member')

        fee_type_id = request.POST.get('fee_type')
        fee_type = FeeType.objects.get(id=fee_type_id) 

        fee_description_id = request.POST.get('fee_description')
        fee_description = FeeDescription.objects.get(id=fee_description_id) 

        outstanding_bill = request.POST.get('outstanding_bill')
        contact = request.POST.get('contact')
        email_address = request.POST.get('email_address')
        user_type = request.POST.get('user_type')
        renewal_period = request.POST.get('renewal_period')
        renewal_bill = request.POST.get('renewal_bill')
        expiration_bill = request.POST.get('expiration_bill')
        total_amount_due = request.POST.get('total_amount_due')
        amount_paid = request.POST.get('amount_paid')
        payment_status = request.POST.get('payment_status')
        arrears=request.POST.get('arrears')


        make_payments = Payments(
                        branch = branch,
                        member_category = member_category,
                        group = group,
                        subgroup = subgroup,
                        member = member,
                        fee_type = fee_type,
                        fee_description = fee_description,
                        outstanding_bill=outstanding_bill,
                        contact=contact,
                        email_address= email_address,
                        user_type=user_type,
                        renewal_period=renewal_period,
                        renewal_bill=renewal_bill,
                        expiration_bill=expiration_bill,
                        total_amount_due=total_amount_due,
                        amount_paid=amount_paid,
                        payment_status=payment_status,
                        arrears=arrears,
                        )
        make_payments.save()  

        invoice_no = f'FMS{year}{month}{day}{make_payments.id}'
        
        make_payments.invoice_no = invoice_no  
        make_payments.save() 

        return HttpResponseRedirect('/view-payments')        
    else:
        return render(request, template_name, {
            'assigned': assigned,
            })
  

def viewPayments(request):
    template_name = 'client/view-payments.html'
    payments = Payments.objects.all().filter(member=member).order_by('-id')
    user = AssignPaymentDuration.objects.all().filter(member=member).first()


    return render(request, template_name, {
        'payments': payments,
        'user': user
    })