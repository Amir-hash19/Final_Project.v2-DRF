from django.urls import path
from .views import CreateInvoiceView, ListUserWithInvoiceView


urlpatterns = [
    path("create-invoice/", CreateInvoiceView.as_view(), name="create-invoice-for-user-by-admin"),
    path("list-user-invoices/", ListUserWithInvoiceView.as_view(), name="list-users-with-invoices"),
]
