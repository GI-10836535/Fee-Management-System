from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( FeeType, FeeItems, FeeDescription, Currency, SetInvoiceDetails, Invoice, AssignPaymentDuration)

class AppAdmin(admin.ModelAdmin):
    pass