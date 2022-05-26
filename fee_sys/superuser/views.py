from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from fee_sys.auth import *
from fee_sys.requests import *
from .models import *
from .forms import *
import requests




# Create your views here.
# Fee Type Views
# Create Fee types
def createFeeType(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        fee_type = request.POST.get('fee_type')

        fee_type = FeeType(fee_type=fee_type)
        fee_type.save()
        return HttpResponseRedirect('/create-fee-type')
    else:
        return render(request, 'superuser/layout.html')


# View fee type
# Edit fee type

# Delete fee type





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
        return HttpResponseRedirect('/create-fee-items')
    else:
        return render(request, 'superuser/create-fee-items.html',{
            'fee_type': FeeType.objects.all().order_by('fee_type'),
        })        

    # if a GET (or any other method) we'll create a blank form
   

# View fee item
# Edit Fee Item
# Delete Fee Item






# Fee Description Views
# Create fee description
def createFeeDescription(request):
    if request.method == 'POST': 
        fee_description = request.POST.get('fee_description')

        fee_description = FeeDescription(fee_description=fee_description)
        fee_description.save()
        return HttpResponseRedirect('/create-fee-description')
    else:

        return render(request, 'superuser/create-fee-description.html')    

# View fee description
# Edit fee description
# Delete fee description





# Currency Views
# Create Currency
def createCurrency(request):
    if request.method == 'POST': 
        currency = request.POST.get('currency')

        currency = Currency(currency=currency)
        currency.save()
        return HttpResponseRedirect('/create-currency')
    else:
        return render(request, 'superuser/create-currency.html')    

# View currency
# Edit Currency
# Delete Currency





# def selectedValue(request):
#     if request.method == 'POST': 
#         selectedValue = request.POST.get('selectedValue')

#         selected_value = SelectedValue(selected_value= selectedValue)
#         selected_value.save()

#         return (request, selectedValue)





def createInvoice(request):
    template_name = 'superuser/invoice.html'

    if request.method == 'POST': 
        branch = request.POST.get('branch')
        member_category = request.POST.get('member_category')
        group = request.POST.get('group')
        subgroup = request.POST.get('subgroup')


        fee_type_id = request.POST.get('fee_type')
        fee_type = FeeType.objects.get(id=fee_type_id)   


        fee_description_id = request.POST.get('fee_description')
        fee_description = FeeDescription.objects.get(id=fee_description_id)


        fee_items_id = request.POST.getlist('fee_items[]')
        int_fee_items = [int(x) for x in fee_items_id]

        for i in int_fee_items:
            fee_items = FeeItems.objects.get(id= i)
    


        items = request.POST.getlist('items_amount[]')
        total_amount = 0

        string_items = [x for x in items if x != ""]
        str1 = [int(x) for x in string_items]
        items_amount = ','.join(str(e) for e in str1)
        for i in str1:
            total_amount += i

            


        invoice = Invoice(branch=branch, member_category=member_category, group=group, subgroup=subgroup, fee_type=fee_type, fee_description=fee_description, fee_items=fee_items, items_amount=items_amount, total_amount=total_amount)
        invoice.save()
        return HttpResponseRedirect('/create-invoice')
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










# # Invoice
# # Create Invoice
# def createInvoiceType(request):
#     template_name = 'superuser/invoice.html'

#     if request.method == 'POST': 
#         branch = request.POST.get('branch')
#         member_category = request.POST.get('member_category')
#         group = request.POST.get('group')
#         subgroup = request.POST.get('subgroup')
#         fee_type = request.POST.get('fee_type')
#         fee_description = request.POST.get('fee_description')


#         fee_items = request.POST.get('fee_items')
#         items_amount = request.POST.get('items_amount')

#         invoice = Invoice(branch=branch, member_category=member_category, group=group, subgroup=subgroup, fee_type=fee_type, fee_description=fee_description,)
#         invoice.save()
#         return HttpResponseRedirect('/create-invoice')
#     else:
#         return render(request, template_name, {
#             'fee_type': FeeType.objects.all(),
#             'fee_items': FeeItems.objects.all(),
#             'fee_description': FeeDescription.objects.all(),
#         }) 



# def createInvoiceItems(request):
#     template_name = 'superuser/invoice.html'
#     f_type = InvoiceType.objects.all().first()
#     fee_type = f_type.fee_type.id
    

#     if request.method == 'POST': 
#         return HttpResponseRedirect('/create-invoice')
#     else:
#         return render(request, template_name, {
#             'fee_items': FeeItems.objects.all().filter(fee_type=fee_type),
#         })     
        


def load_fee_items(request):
    template_name = 'superuser/invoice.html'

    if request.method == 'GET': 
        selectedValue = request.POST.get('fee_type')
        selected_value = FeeItems.objects.filter(fee_type=selectedValue)
        

        return (request, template_name, {"selected_value":selected_value})
            
      

         

# View invoice
# Edit invoice
# Delete invoice


def setInvoiceDetails(request):
    if request.method == "POST":
        signers_name = request.POST.get('signers_name')
        signature = request.FILES.get('signature')
        logo = request.FILES.get('logo')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        invoice_details = SetInvoiceDetails(signers_name=signers_name, signature=signature, logo=logo, contact=contact, email=email)
        invoice_details.save()
        return HttpResponseRedirect('/set-invoice')
    else:
        return render(request, 'superuser/set-invoice.html')    




def assignPaymentDuration(request):
    template_name = 'superuser/assign-payment.html'

    if request.method == 'POST':
        branch = request.POST.get('branch')
        member_category = request.POST.get('member_category')
        group = request.POST.get('group')
        subgroup = request.POST.get('subgroup')
        member = request.POST.get('member')
        fee_type = request.POST.get('fee_type')
        total_invoice = request.POST.get('total_invoice')
        install_days = request.POST.get('install_days')
        install_amount = request.POST.get('install_amount')
        set_date =  request.POST.get('set_date')
        start_date =  request.POST.get('start_date')
        end_date =  request.POST.get('end_date')
        account_status = request.POST.get('account_status')

        assignPayment = AssignPaymentDuration(
                        branch = branch,
                        member_category = member_category,
                        group = group,
                        subgroup = subgroup,
                        member =member,
                        fee_type = fee_type,
                        total_invoice = total_invoice,
                        install_days = install_days,
                        install_amount = install_amount,
                        set_date =  set_date,
                        start_date =  start_date,
                        end_date =  end_date,
                        account_status = account_status
        )
        assignPayment.save()
        return HttpResponseRedirect('/assign-payment')
    else:
        return render(request, template_name, {
            'invoice': Invoice.objects.all(),
            'fee_type': FeeItems.objects.all(),
            'member_categories': member_categories,
            'branches':branches,
            'groups': groups,
            'subgroups': subgroups,
        })   
