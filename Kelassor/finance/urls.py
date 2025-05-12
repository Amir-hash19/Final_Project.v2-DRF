from django.urls import path
from .views import CreateInvoiceView, ListUserWithInvoiceView, DeleteInvoiceView, CreatePaymentView


urlpatterns = [
    path("create-invoice/", CreateInvoiceView.as_view(), name="create-invoice-for-user-by-admin"),
    path("list-user-invoices/", ListUserWithInvoiceView.as_view(), name="list-users-with-invoices"),
    path("delete-invoice/<slug:slug>/", DeleteInvoiceView.as_view(), name="delete-invoice-by-admin"),
    path("create/<slug:slug>/payment/", CreatePaymentView.as_view(), name="create-payment"),
]
