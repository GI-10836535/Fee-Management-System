# from django import views
from django.urls import path
from . import views

app_name = 'superuser'

urlpatterns = [
    path('', views.index, name="index"),

    path('create-fee-type/', views.createFeeType, name="createFeeType"),
    path('view-fee-type/', views.viewFeeType, name="viewFeeType"),
    path('edit-fee-type/<int:id>', views.editFeeType, name='editFeeType'),
    path('delete-fee-type/<int:id>', views.deleteFeeType, name='deleteFeeType'),


    path('create-fee-items/', views.createFeeItems, name="createFeeItems"),
    path('view-fee-items/', views.viewFeeItems, name="viewFeeItems"),
    path('edit-fee-item/<int:id>', views.editFeeItem, name='editFeeItem'),
    path('delete-fee-item/<int:id>', views.deleteFeeItem, name='deleteFeeItem'),


    path('create-fee-description/', views.createFeeDescription, name="createFeeDescription"),
    path('view-fee-description/', views.viewFeeDescription, name="viewFeeDescription"),
    path('edit-fee-description/<int:id>', views.editFeeDescription, name='editFeeDescription'),
    path('delete-fee-description/<int:id>', views.deleteFeeDescription, name='deleteFeeDescription'),


    path('create-currency/', views.createCurrency, name="createCurrency"),
    path('view-currency/', views.viewCurrency, name="viewCurrency"),
    path('edit-currency/<int:id>', views.editCurrency, name='editCurrency'),
    path('delete-currency/<int:id>', views.deleteCurrency, name='deleteCurrency'),


    path('set-invoice-details/', views.setInvoiceDetails, name="setInvoiceDetails"),
    path('view-invoice-details/', views.viewInvoiceDetails, name="viewInvoiceDetails"),
    path('edit-invoice-details/<int:id>', views.editInvoiceDetails, name='editInvoiceDetails'),
    path('delete-invoice-details/<int:id>', views.deleteInvoiceDetails, name='deleteInvoiceDetails'),


    path('create-invoice/', views.createInvoice, name="createInvoice"),
    path('view-invoice/', views.viewInvoice, name="viewInvoice"),
    path('edit-invoice/<int:id>', views.editInvoice, name='editInvoice'),
    path('delete-invoice/<int:id>', views.deleteInvoice, name='deleteInvoice'),


    path('assign-payment/', views.assignPaymentDuration, name="assignPaymentDuration"),
    path('assign-payments/<pk>', views.assignPaymentsDuration, name="assignPaymentsDuration"),
    path('view-payment-details/', views.viewPaymentDuration, name="viewPaymentDuration"),
    path('delete-invoice/<int:id>', views.deletePaymentDuration, name='deletePaymentDuration'),


    path('ajax/load-items/', views.load_items, name='ajax_load_items'),
    path('ajax/load-invoice/', views.load_invoice, name='ajax_load_invoice'),
    path('ajax/load_balance/', views.load_balance, name='ajax_load_balance'),
    path('ajax/load_fee/', views.load_fee, name='ajax_load_fee'),

    path('make-payment/', views.makePayment, name="makePayment"),
    path('make-payments/<pk>', views.makePayments, name="makePayments"),
    path('view-payments/', views.viewPayments, name="viewPayments"),
    path('invoice-details-view/<pk>', views.invoice_details_view, name="invoice_details_view"),

    

    # path('create-invoice-it/', views.createInvoiceType, name="createInvoiceType"),
    # path('home/', views.home, name="home"),
]