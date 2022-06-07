from django import views
from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.index, name="index"),
    path('view-assigned-payments/', views.viewAssignedPayments, name="viewAssignedPayments"),
    path('make-payments/<pk>', views.makePayments, name="makePayments"),
    path('view-payments/', views.viewPayments, name="viewPayments"),
    path('invoice-details-view/<pk>', views.invoice_details_view, name="invoice_details_view"),

    # path('home/', views.home, name="home"),
]