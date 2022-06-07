from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( AssignPeriod, FeeType, FeeItems, FeeDescription, Currency, InvoiceDetails, Invoice, AssignPaymentDuration, MakePayment)

class AppAdmin(admin.ModelAdmin):
    pass