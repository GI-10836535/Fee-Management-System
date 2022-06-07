from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from fee_sys.auth import *
from fee_sys.requests import *
from .models import *
from .forms import *
import requests
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from .filter import *

# PDF stuff
from django.template.loader import get_template
from xhtml2pdf import pisa

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter






def invoice_details_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    company = InvoiceDetails.objects.get(pk=1)
    detail = get_object_or_404(MakePayment, pk=pk)
    # items = get_object_or_404(FeeItems, pk=pk)

    # temp_invoice = [int(invoice.total_amount) for invoice in Invoice.objects.all()]
    invoice = Invoice.objects.get(fee_type= detail.fee_type, branch= detail.branch, member_category= detail.member_category, group= detail.group, subgroup= detail.subgroup)

    keys = [item.fee_items for item in invoice.fee_items.all()]
    values = [int(i) for i in invoice.items_amount.split(',')]
    data = dict(zip(keys, values))

    template_path = 'superuser/user_printer.html'
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
    template_name = 'superuser/index.html'
    invoices = Invoice.objects.all()
    assigned_payments = AssignPaymentDuration.objects.all()
    payments = MakePayment.objects.all()
    total_invoice = 0
    total_payments = 0
    total_arrears = 0
    total_users = 0


    temp_invoice = [int(invoice.total_amount) for invoice in Invoice.objects.all()]
    temp_payments = [int(payment.amount_paid) for payment in MakePayment.objects.all()]
    temp_arrears = [int(payment.arrears) for payment in MakePayment.objects.all()]

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



# Create your views here.

# Fee Type Views
# Create Fee types
def createFeeType(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        fee_type = request.POST.get('fee_type')

        fee_type = FeeType(fee_type=fee_type)
        fee_type.save()
        return HttpResponseRedirect('/view-fee-type')
    else:
        return render(request, 'superuser/create-fee-type.html')


# View fee type
def viewFeeType(request):
    template_name = 'superuser/view-fee-type.html'
    return render(request, template_name, {
        'fee_types': FeeType.objects.all()
    })


# Edit fee type
def editFeeType(request, id):

    fee_type = FeeType.objects.get(id=id)
    
    if request.method == 'POST':
        fee_type.fee_type = request.POST.get('fee_type')
        fee_type.save()

        return HttpResponseRedirect('/view-fee-type')

    return render(request, 'superuser/edit-fee-type.html', {
        'fee_type': fee_type,
        'fee_types': FeeType.objects.all().order_by('fee_type'),
    }) 
    

# Delete fee type
def deleteFeeType(request, id):
    fee_type = FeeType.objects.get(id=id)
    fee_type.delete()
    return HttpResponseRedirect('/view-fee-type')

    




# Fee Items views
# Create Fee item
def createFeeItems(request):

    if request.method == 'POST':
        fee_type = request.POST.get('fee_type')
        fee_items = request.POST.get('fee_items')
        # check whether it's valid:

        r = FeeType.objects.get(id=fee_type)

        fee_items = FeeItems(fee_type=r, fee_items=fee_items)
        fee_items.save()
        return HttpResponseRedirect('/view-fee-items')
    else:
        return render(request, 'superuser/create-fee-items.html',{
            'fee_type': FeeType.objects.all().order_by('fee_type'),
        })        

   

# View fee item
def viewFeeItems(request):
    template_name = 'superuser/view-fee-items.html'
    fee_type = FeeType.objects.all()

    for i in fee_type:
        fee_itemss = FeeItems.objects.filter(fee_type=i)

    return render(request, template_name, {
        'fee_items': FeeItems.objects.all().order_by('-fee_type')
    })


# Edit Fee Item
def editFeeItem(request, id):
    template_name = 'superuser/edit-fee-item.html'

    fee_item = FeeItems.objects.get(id=id)
    
    if request.method == 'POST':
        fee_type = request.POST.get('fee_type')
        fee_item.fee_type = FeeType.objects.get(id=fee_type)

        fee_item.fee_items = request.POST.get('fee_items')

        fee_item.save()

        return HttpResponseRedirect('/view-fee-items')

    return render(request, template_name, {
        'fee_item': fee_item,
        'fee_types': FeeType.objects.all().order_by('-fee_type'),
    }) 



# Delete Fee Item
def deleteFeeItem(request, id):
    fee_item = FeeItems.objects.get(id=id)
    fee_item.delete()
    return HttpResponseRedirect('/view-fee-items')






# Fee Description Views
# Create fee description
def createFeeDescription(request):
    if request.method == 'POST': 
        fee_description = request.POST.get('fee_description')

        fee_description = FeeDescription(fee_description=fee_description)
        fee_description.save()
        return HttpResponseRedirect('/view-fee-description')
    else:

        return render(request, 'superuser/create-fee-description.html')    


# View fee description
def viewFeeDescription(request):
    template_name = 'superuser/view-fee-description.html'

    return render(request, template_name, {
        'fee_descriptions': FeeDescription.objects.all()
    })


# Edit fee description
def editFeeDescription(request, id):

    fee_description = FeeDescription.objects.get(id=id)
    
    if request.method == 'POST':
        fee_description.fee_description = request.POST.get('fee_description')
        fee_description.save()

        return HttpResponseRedirect('/view-fee-description')

    return render(request, 'superuser/edit-fee-description.html', {
        'fee_description': fee_description,
        # 'fee_types': FeeType.objects.all().order_by('fee_type'),
    }) 
  

# Delete fee description
def deleteFeeDescription(request, id):
    fee_description = FeeDescription.objects.get(id=id)
    fee_description.delete()
    return HttpResponseRedirect('/view-fee-description')




# Currency Views
# Create Currency
def createCurrency(request):
    if request.method == 'POST': 
        currency = request.POST.get('currency')

        currency = Currency(currency=currency)
        currency.save()
        return HttpResponseRedirect('/view-currency')
    else:
        return render(request, 'superuser/create-currency.html')    


# View currency
def viewCurrency(request):
    template_name = 'superuser/view-currency.html'

    return render(request, template_name, {
        'currencies': Currency.objects.all()
    })


# Edit Currency
def editCurrency(request, id):
    template_name = 'superuser/edit-currency.html'

    currency = Currency.objects.get(id=id)
    
    if request.method == 'POST':
        currency.currency = request.POST.get('currency')
        currency.save()
        return HttpResponseRedirect('/view-currency')

    return render(request, template_name, {
        'currency': currency,
    }) 
  

# Delete Currency
def deleteCurrency(request, id):
    currency = Currency.objects.get(id=id)
    currency.delete()
    return HttpResponseRedirect('/view-currency')




# Invoice
def createInvoice(request):
    template_name = 'superuser/create-invoice.html'

    if request.method == 'POST': 
        branch = request.POST.get('branch')
        member_category = request.POST.get('member_category')
        group = request.POST.get('group')
        subgroup = request.POST.get('subgroup')


        fee_type_id = request.POST.get('fee_type')
        fee_type = FeeType.objects.get(id=fee_type_id)   


        fee_description_id = request.POST.get('fee_description')
        fee_description = FeeDescription.objects.get(id=fee_description_id)

        items = request.POST.getlist('items_amount[]')
        total_amount = 0

        string_items = [x for x in items if x != ""]
        str1 = [int(x) for x in string_items]
        items_amount = ','.join(str(e) for e in str1)
        for i in str1:
            total_amount += i

            

        invoice = Invoice.objects.create(branch=branch, member_category=member_category, group=group, subgroup=subgroup, fee_type=fee_type, fee_description=fee_description, items_amount=items_amount, total_amount=total_amount)
        invoice.save()

        fee_items_names = [x.fee_items for x in FeeItems.objects.all()]
        fee_items_ids = []

        for x in fee_items_names:
                fee_items_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("pass")

        for i in fee_items_ids:
            invoice.fee_items.add(FeeItems.objects.get(id=i))
            
        
         
        return HttpResponseRedirect('/view-invoice')
    else:
        return render(request, template_name, {
            'fee_type': FeeType.objects.all(),
            'fee_items': FeeItems.objects.all(),
            'fee_description': FeeDescription.objects.all(),
            'member_categories': member_categories,
            'branches':branches,
            'groups': groups,
            'subgroups': subgroups,
        }) 

  

def load_items(request):
    template_name = 'superuser/test.html'

    if request.method == 'GET': 
        fee_type = request.GET.get('fee_type')
        fee_items = FeeItems.objects.filter(fee_type=fee_type).order_by('fee_type')
        return render(request, template_name, {'fee_items': fee_items})

         
# View invoice
def viewInvoice(request):
    template_name = 'superuser/view-invoice.html'

    return render(request, template_name, {
        'invoices': Invoice.objects.all().order_by('-id')
    })


# Edit invoice
def editInvoice(request, id):
    template_name = 'superuser/edit-invoice.html'
    
    invoice = Invoice.objects.get(id=id)
    
    if request.method == 'POST':
        invoice.branch = request.POST.get('branch')
        invoice.member_category = request.POST.get('member_category')
        invoice.group = request.POST.get('group')
        invoice.subgroup = request.POST.get('subgroup')
        invoice.fee_type = request.POST.get('fee_type')
        invoice.fee_description = request.POST.get('fee_description')

        invoice.fee_items = request.POST.getlist('fee_items[]')

        items = request.POST.getlist('items_amount[]')
        invoice.total_amount = 0

        string_items = [x for x in items if x != ""]
        str1 = [int(x) for x in string_items]

        invoice.items_amount = ','.join(str(e) for e in str1)
        for i in str1:
            invoice.total_amount += i

        invoice.save()
        return HttpResponseRedirect('/view-currency')


    return render(request, template_name, {
        'invoice': invoice,
        'fee_type': FeeType.objects.all(),
        'fee_items': FeeItems.objects.all(),
        'fee_description': FeeDescription.objects.all(),            
        'member_categories': member_categories,
        'branches':branches,
        'groups': groups,
        'subgroups': subgroups,
    }) 

# Delete invoice
def deleteInvoice(request, id):
    invoice = Invoice.objects.get(id=id)
    invoice.delete()
    return HttpResponseRedirect('/view-invoice')





# Create Invoice Details
def setInvoiceDetails(request):
    if request.method == "POST":
        signers_name = request.POST.get('signers_name')
        company_name = request.POST.get('company_name')
        signature = request.FILES.get('signature')
        logo = request.FILES.get('logo')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        invoice_details = InvoiceDetails(signers_name=signers_name, company_name=company_name, signature=signature, logo=logo, contact=contact, email=email)
        invoice_details.save()
        return HttpResponseRedirect('/set-invoice')
    else:
        return render(request, 'superuser/set-invoice.html')    


# View Invoice Details
def viewInvoiceDetails(request):
    template_name = 'superuser/view-invoice-details.html'

    return render(request, template_name, {
        'invoice_details': InvoiceDetails.objects.all()
    })

# Edit invoice details
def editInvoiceDetails(request, id):
    template_name = 'superuser/edit-invoice-details.html'

    invoice_detail = InvoiceDetails.objects.get(id=id)
    
    if request.method == 'POST':
        invoice_detail.signers_name = request.POST.get('signers_name')
        invoice_detail.signature = request.FILES.get('signature')
        invoice_detail.logo = request.FILES.get('logo')
        invoice_detail.contact = request.POST.get('contact')
        invoice_detail.email = request.POST.get('email')

        invoice_detail.save()
        return HttpResponseRedirect('/view-invoice-details')

    return render(request, template_name, {
        'invoice_detail': invoice_detail,
    }) 


# Delete Invoice Details
def deleteInvoiceDetails(request, id):
    invoice_detail = InvoiceDetails.objects.get(id=id)
    invoice_detail.delete()
    return HttpResponseRedirect('/view-invoice-details')






# Assign Payment
# Create Payment Duration
def assignPaymentDuration(request):
    template_name = 'superuser/assign-payment.html'

    if request.method == 'POST':
        branch = request.POST.get('branch')
        member_category = request.POST.get('member_category')
        group = request.POST.get('group')
        subgroup = request.POST.get('subgroup')
        member = request.POST.get('member')

        # fee_type = request.POST.get('fee_type')
        fee_type_id = request.POST.get('fee_type')
        fee_type = FeeType.objects.get(id=fee_type_id) 

        fee_description_id = request.POST.get('fee_description')
        fee_description = FeeDescription.objects.get(id=fee_description_id) 

        total_invoice = request.POST.get('total_invoice')
        install_range = request.POST.get('install_range')
        install_period = request.POST.get('install_period')
        install_amount = request.POST.get('install_amount')
        set_pay_date =  request.POST.get('set_pay_date')
        start_date =  request.POST.get('start_date')
        end_date =  request.POST.get('end_date')
        account_status = request.POST.get('account_status')

        if set_pay_date != "":
            deadline = set_pay_date
        else:
            if install_range == 'Days(s)':
                deadline = datetime.now() + timedelta(days=int(install_period))
            elif install_range == 'Month(s)':
                deadline = datetime.today()+ relativedelta(months=int(install_period)) 
            elif install_range == 'Years(s)':
                deadline = datetime.today()+ relativedelta(years=int(install_period)) 
            else:
                pass


        assignPayment = AssignPaymentDuration(
                        branch = branch,
                        member_category = member_category,
                        group = group,
                        subgroup = subgroup,
                        member = member,
                        fee_type = fee_type,
                        fee_description = fee_description,
                        total_invoice = total_invoice,
                        install_range = install_range,
                        install_period = install_period,
                        install_amount = install_amount,
                        set_pay_date =  set_pay_date,
                        start_date =  start_date,
                        end_date =  end_date,
                        account_status = account_status,
                        deadline=deadline
                        
        )
        assignPayment.save()
        return HttpResponseRedirect('/view-payment-details')
    else:
        return render(request, template_name, {
            'invoice': Invoice.objects.all(),
            'fee_types': FeeType.objects.all(),
            'fee_descriptions': FeeDescription.objects.all(),
            'period': AssignPeriod.objects.all(),
            'member_categories': member_categories,
            'branches':branches,
            'groups': groups,
            'subgroups': subgroups,
            'members': members,
        })   



# Auto assign
def assignPaymentsDuration(request, **kwargs):
    template_name = 'superuser/assign-payments.html'
    pk = kwargs.get('pk')
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        branch = request.POST.get('branch')
        member_category = request.POST.get('member_category')
        group = request.POST.get('group')
        subgroup = request.POST.get('subgroup')
        member = request.POST.get('member')

        # fee_type = request.POST.get('fee_type')
        fee_type_id = request.POST.get('fee_type')
        fee_type = FeeType.objects.get(id=fee_type_id) 

        fee_description_id = request.POST.get('fee_description')
        fee_description = FeeDescription.objects.get(id=fee_description_id) 

        total_invoice = request.POST.get('total_invoice')
        install_range = request.POST.get('install_range')
        install_period = request.POST.get('install_period')
        install_amount = request.POST.get('install_amount')
        set_pay_date =  request.POST.get('set_pay_date')
        start_date =  request.POST.get('start_date')
        end_date =  request.POST.get('end_date')
        account_status = request.POST.get('account_status')

        if set_pay_date != "":
            deadline = set_pay_date
        else:
            if install_range == 'Days(s)':
                deadline = datetime.now() + timedelta(days=int(install_period))
            elif install_range == 'Month(s)':
                deadline = datetime.today()+ relativedelta(months=int(install_period)) 
            elif install_range == 'Years(s)':
                deadline = datetime.today()+ relativedelta(years=int(install_period)) 
            else:
                pass


        assignPayments = AssignPaymentDuration(
                        branch = branch,
                        member_category = member_category,
                        group = group,
                        subgroup = subgroup,
                        member = member,
                        fee_type = fee_type,
                        fee_description = fee_description,
                        total_invoice = total_invoice,
                        install_range = install_range,
                        install_period = install_period,
                        install_amount = install_amount,
                        set_pay_date =  set_pay_date,
                        start_date =  start_date,
                        end_date =  end_date,
                        account_status = account_status,
                        deadline=deadline             
        )
        assignPayments.save()
        return HttpResponseRedirect('/view-payment-details')
    else:
        return render(request, template_name, {
            'invoice': invoice,
            'period': AssignPeriod.objects.all()
        })   






def load_invoice(request):
    template_name = 'superuser/test2.html'
    data = []
    amounts = []

    if request.method == 'GET': 
        branch = request.GET.get('branch')
        member_category = request.GET.get('member_category')
        group = request.GET.get('group')
        subgroup = request.GET.get('subgroup')
        fee_type = request.GET.get('fee_type')
        total_invoice = Invoice.objects.filter(fee_type=fee_type, branch=branch, member_category=member_category, group=group, subgroup=subgroup)
        
        for i in total_invoice.values():
             data.append(i)
        for x in range(len(data)):
             amounts.append(data[x]['total_amount']) 
        # print(amounts) 

        amount = [int(k) for k in amounts]

        return render(request, template_name, {
            'total_invoice': total_invoice,
            'amount': amount 
            })



# View Payment Durations  
def viewPaymentDuration(request):
    template_name = 'superuser/view-payment-details.html'

    if request.method == 'GET':
        assigned_payments = AssignPaymentDuration.objects.all().order_by('-id')
        my_filter = AssignPaymentDurationFilter(request.GET, queryset=assigned_payments)
        assigned_payments = my_filter.qs

        s = Paginator(assigned_payments, 3)
        page = request.GET.get('page')
        assigned_payments = s.get_page(page)

    return render(request, template_name, {
        'my_filter': my_filter,
        'assigned_payments': assigned_payments,
    }) 

# Delete payment duration
def deletePaymentDuration(request, id):
    payment_duration = AssignPaymentDuration.objects.get(id=id)
    payment_duration.delete()
    return HttpResponseRedirect('/view-payment-details')




# Make payments
# create payments
def makePayment(request):
    template_name = 'superuser/make-payment.html'

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
        payers_first_name = request.POST.get('payers_first_name')
        payers_last_name = request.POST.get('payers_last_name')
        contact = request.POST.get('contact')
        email_address = request.POST.get('email_address')
        remarks = request.POST.get('remarks')
        user_type = request.POST.get('user_type')
        renewal_period = request.POST.get('renewal_period')
        renewal_bill = request.POST.get('renewal_bill')
        expiration_bill = request.POST.get('expiration_bill')
        total_amount_due = request.POST.get('total_amount_due')
        amount_paid = request.POST.get('amount_paid')
        payment_status = request.POST.get('payment_status')
        arrears=request.POST.get('arrears')



        make_payment = MakePayment(
                        branch = branch,
                        member_category = member_category,
                        group = group,
                        subgroup = subgroup,
                        member = member,
                        fee_type = fee_type,
                        fee_description=fee_description,
                        outstanding_bill=outstanding_bill,
                        payers_first_name = payers_first_name,
                        payers_last_name = payers_last_name,
                        contact=contact,
                        email_address= email_address,
                        remarks=remarks,
                        user_type=user_type,
                        renewal_period=renewal_period,
                        renewal_bill=renewal_bill,
                        expiration_bill=expiration_bill,
                        total_amount_due=total_amount_due,
                        amount_paid=amount_paid,
                        payment_status=payment_status,
                        arrears=arrears,
                        )
        make_payment.save()  

        user_balance = AssignPaymentDuration.objects.filter(member=member, fee_type=fee_type) 
          

        return HttpResponseRedirect('/view-payments')        
    else:
        return render(request, template_name, {
            'branches':branches,
            'member_categories': member_categories,
            'groups': groups,
            'subgroups': subgroups,
            'members': members,
            'fee_type': FeeType.objects.all(),
            'fee_description': FeeDescription.objects.all(),
            'invoice': Invoice.objects.all(),
            'payment_duration': AssignPaymentDuration.objects.all(),  
        })




def makePayments(request, **kwargs):
    template_name = 'superuser/make-payment-2.html'
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
        payers_first_name = request.POST.get('payers_first_name')
        payers_last_name = request.POST.get('payers_last_name')
        contact = request.POST.get('contact')
        email_address = request.POST.get('email_address')
        remarks = request.POST.get('remarks')
        user_type = request.POST.get('user_type')
        renewal_period = request.POST.get('renewal_period')
        renewal_bill = request.POST.get('renewal_bill')
        expiration_bill = request.POST.get('expiration_bill')
        total_amount_due = request.POST.get('total_amount_due')
        amount_paid = request.POST.get('amount_paid')
        payment_status = request.POST.get('payment_status')
        arrears=request.POST.get('arrears')


        make_payments = MakePayment(
                        branch = branch,
                        member_category = member_category,
                        group = group,
                        subgroup = subgroup,
                        member = member,
                        fee_type = fee_type,
                        fee_description=fee_description,
                        outstanding_bill=outstanding_bill,
                        payers_first_name = payers_first_name,
                        payers_last_name = payers_last_name,
                        contact=contact,
                        email_address= email_address,
                        remarks=remarks,
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
        return render(request, template_name, {'assigned': assigned,})




def load_fee(request):
    template_name = 'superuser/member-fee-type.html'
    fee_types =[]

    if request.method == 'GET': 
        member = request.GET.get('member')

        user_type = AssignPaymentDuration.objects.filter(member=member)
        item = []
        items = []

        for i in user_type.values():   
            item.append(i)
        for x in range(len(item)):
            items.append(item[x]['fee_type_id'])    
        
        for k in items:
            fee_types.append(FeeType.objects.get(id=int(k))) 
        
        return render(request, template_name, {
            'fee_types' : fee_types,
            'user_type' : user_type,
            })



def load_balance(request):
    template_name = 'superuser/member-payment.html'
    fee_type = FeeType.objects.all()


    if request.method == 'GET': 
        fee_type = request.GET.get('fee_type')
        member = request.GET.get('member')
        balance = AssignPaymentDuration.objects.filter(member=member, fee_type=fee_type)

        # print(f'{fee_type}-{member}')

        return render(request, template_name, {
            'balance' : balance,
            })



def viewPayments(request):
    template_name = 'superuser/view-payments.html'
    today = date.today()
    # print("Today's date:", today)

    if request.method == 'GET':
        payments = MakePayment.objects.all().order_by('-id')
        payment_filter = PaymentsFilter(request.GET, queryset=payments)
        payments = payment_filter.qs

        p = Paginator(payments, 3)
        page = request.GET.get('page')
        payments = p.get_page(page)
 
    return render(request, template_name, {
        'payment_filter': payment_filter,
        'payments': payments,
        'today': today,
    }) 


