# from django import views
from django.urls import path
from . import views

app_name = 'superuser'

urlpatterns = [
    path('create-fee-type/', views.createFeeType, name="createFeeType"),
    path('create-fee-items/', views.createFeeItems, name="createFeeItems"),
    path('create-fee-description/', views.createFeeDescription, name="createFeeDescription"),
    path('create-currency/', views.createCurrency, name="createCurrency"),
    path('set-invoice/', views.setInvoiceDetails, name="setInvoiceDetails"),
    path('invoice/', views.createInvoice, name="createInvoice"),
    path('assign-payment/', views.assignPaymentDuration, name="assignPaymentDuration"),
    path('load-fee-items/', views.load_fee_items, name="load_fee_items"),
    # path('create-invoice-it/', views.createInvoiceType, name="createInvoiceType"),
    # path('home/', views.home, name="home"),
]