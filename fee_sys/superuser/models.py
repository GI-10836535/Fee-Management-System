from django.db import models
from django.forms import ModelForm
from django import forms
from datetime import date
from django.utils import timezone
# from .views import increment_invoice_number


# Create your models here.

class FeeType(models.Model):
    id = models.AutoField(primary_key=True)
    fee_type = models.CharField(max_length= 50)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.fee_type}'


class FeeItems(models.Model):
    id = models.AutoField(primary_key=True)
    fee_type = models.ForeignKey(FeeType, on_delete= models.CASCADE)
    fee_items = models.CharField(max_length = 100)
    date_created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f'{self.fee_items}'


class FeeDescription(models.Model):
    id = models.AutoField(primary_key=True)
    fee_description = models.CharField(max_length= 100)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.fee_description



class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length= 100)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.currency



class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length= 100)
    member_category = models.CharField(max_length= 100)
    group = models.CharField(max_length= 100)
    subgroup = models.CharField(max_length= 100)
    fee_type = models.ForeignKey(FeeType, on_delete= models.SET_NULL, null=True)
    fee_description = models.ForeignKey(FeeDescription, on_delete= models.SET_NULL, null=True)
    fee_items = models.ManyToManyField(FeeItems)
    items_amount = models.CharField(max_length= 100)
    total_amount = models.IntegerField(default=0, null=True)
    date_created = models.DateTimeField(auto_now_add= True)



    def __str__(self):
        return f'{self.branch}, {self.member_category}, {self.group}, {self.subgroup}, {self.fee_type}, {self.fee_description},'




# logo and signature upload

class InvoiceDetails(models.Model):
    id = models.AutoField(primary_key=True)
    signers_name = models.CharField(max_length= 500)
    company_name = models.CharField(max_length= 500, default="Akwaaba Solutions Agency", null=True)
    signature = models.ImageField(blank=True, null=True, upload_to='signature-uploads/', default='')
    logo = models.ImageField(blank=True, null=True, upload_to='logo-uploads/', default='')
    contact = models.CharField(max_length= 500)
    email = models.EmailField(max_length= 500)


    def __str__(self):
        return f'{self.signers_name}, {self.contact}'



class AssignPeriod(models.Model):
    name = models.CharField(max_length= 100)

    def __str__(self):
        return f'{self.name}'


class AssignPaymentDuration(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length= 100, null=True)
    member_category = models.CharField(max_length= 100, null=True)
    group = models.CharField(max_length= 100, null=True)
    subgroup = models.CharField(max_length= 100, null=True)
    member = models.CharField(max_length= 100, null=True)
    fee_type = models.ForeignKey(FeeType, on_delete= models.SET_NULL, null=True)
    fee_description = models.ForeignKey(FeeDescription, on_delete= models.SET_NULL, null=True)
    total_invoice = models.IntegerField(blank=True, null=True)
    install_range = models.CharField(max_length= 100, default= None)
    install_period = models.IntegerField(blank=True, null=True)
    install_amount = models.IntegerField(blank=True, null=True)
    set_pay_date =  models.DateField(blank=True, null=True, default=timezone.now)
    start_date =  models.DateField(blank=True, null=True)
    end_date =  models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    account_status = models.CharField(max_length= 100)
    date_created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f'{self.member} - {self.total_invoice}, {self.fee_type}'


class MakePayment(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length= 100, null=True)
    member_category = models.CharField(max_length= 100, null=True)
    group = models.CharField(max_length= 100, null=True)
    subgroup = models.CharField(max_length= 100, null=True)
    member = models.CharField(max_length= 100, null=True)
    fee_type = models.ForeignKey(FeeType, on_delete= models.SET_NULL, null=True)
    fee_description = models.ForeignKey(FeeDescription, on_delete= models.SET_NULL, null=True)
    outstanding_bill = models.IntegerField(blank=True, null=True)
    payers_first_name = models.CharField(max_length= 100, null=True)
    payers_last_name = models.CharField(max_length= 100, null=True)
    contact = models.CharField(max_length= 100, null=True)
    email_address = models.EmailField(max_length= 500, null=True)
    remarks = models.CharField(max_length= 100, null=True)
    user_type = models.CharField(max_length= 100, null=True)
    renewal_period = models.CharField(max_length=100,  null=True)
    renewal_bill = models.IntegerField(blank=True, null=True)
    expiration_bill = models.IntegerField(blank=True, null=True)
    total_amount_due = models.IntegerField(blank=True, null=True)
    amount_paid = models.IntegerField(blank=True, null=True)
    payment_status = models.CharField(max_length=100, null=True)
    arrears = models.IntegerField(blank=True, null=True)
    end_date =  models.DateField(blank=True, null=True, default=timezone.now)
    date_created = models.DateTimeField(auto_now_add= True)
    invoice_no = models.CharField(max_length=500, default="FMS2022661", null=True, blank=True)


    def __str__(self):
        return f"{self.payers_first_name} {self.payers_last_name} paid for {self.member}-{self.total_amount_due}, {self.payment_status}"