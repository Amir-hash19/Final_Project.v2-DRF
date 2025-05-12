from django.urls import path
from .views import CreateInvoiceView


urlpatterns = [
    path("create-invoice/", CreateInvoiceView.as_view(), name="create-invoice-for-user-by-admin"),
]
