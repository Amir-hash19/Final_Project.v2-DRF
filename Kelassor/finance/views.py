from .models import Payment, Invoice, Transaction
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from account.permissions import GroupPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status 
from account.views import CustomPagination
from account.models import CustomUser
from .serializers import InvoiceSerializer, BasicUserSerializer
from django.db.models import Count



class CreateInvoiceView(CreateAPIView):
    permission_classes = [IsAuthenticated ,GroupPermission("SupportPanel", "SuperUser")]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer



class ListUserWithInvoiceView(ListAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BasicUserSerializer

    def get_queryset(self):
        return  CustomUser.objects.annotate(invoice_count=Count('invoice')).filter(invoice_count__gt=0)



class DeleteInvoiceView(DestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer     
    lookup_field = 'slug'   