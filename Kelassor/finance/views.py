from .models import Payment, Invoice, Transaction
from rest_framework.generics import CreateAPIView, ListAPIView
from account.permissions import GroupPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status 
from account.views import CustomPagination
from .serializers import InvoiceSerializer




class CreateInvoiceView(CreateAPIView):
    permission_classes = [IsAuthenticated ,GroupPermission("SupportPanel", "SuperUser")]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer



