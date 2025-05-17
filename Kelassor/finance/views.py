from .models import Payment, Invoice, Transaction
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from account.permissions import GroupPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status 
from account.views import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from account.views import CustomPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import transaction
from rest_framework.exceptions import ValidationError
from account.models import CustomUser
from django.db.models import Sum
from .serializers import (InvoiceSerializer, BasicUserSerializer, PaymentSerializer, TransactionSerializer, 
                          InvoiceUpdateSerializer)
from django.db.models import Count






class CreateInvoiceView(CreateAPIView):
    permission_classes = [IsAuthenticated ,GroupPermission("SupportPanel", "SuperUser")]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer





class ListUserWithInvoiceView(ListAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BasicUserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = CustomPagination

    def get_queryset(self):
        return  CustomUser.objects.annotate(invoice_count=Count('invoice')).filter(invoice_count__gt=0)



class DeleteInvoiceView(DestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer     
    lookup_field = 'slug'   



class CreatePaymentView(CreateAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]


    def perform_create(self, serializer):
        with transaction.atomic():
            invoice_slug = self.kwargs.get('slug')
            try:
                invoice = Invoice.objects.select_for_update().get(slug=invoice_slug)
            except Invoice.DoesNotExist:
                raise ValidationError({"invoice":"the invoice does not existed!"})

            total_paid = invoice.payments.filter(is_verified=True).aggregate(
                total=Sum('amount'))['total'] or 0

            new_payment_amount = serializer.validated_data['amount']

            if total_paid + new_payment_amount > invoice.amount:
                raise ValidationError("This payment is exceeds the invoice total")


            if invoice.client != self.request.user:
                raise ValidationError("You can only select your invoice")


            payment = serializer.save(user=self.request.user, invoice=invoice)

            
            if total_paid + new_payment_amount >= invoice.amount:
                invoice.is_paid = True
                invoice.save()

            




class AdminListPaymentView(ListAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = PaymentSerializer

    


class ListPaymentView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["amount", "invoice"]
    filterset_fields = ["method", "paid_at"]
    ordering_fields = ["-paid_at"]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    


class ListTransactionView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "amount"]
    filterset_fields = ["transaction_type", "transaction_date"]
    ordering_fields = ["-transaction_date"]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    


class EditInvoicesView(UpdateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceUpdateSerializer
    lookup_field = 'slug'





class ListInvoiceUserView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "amount"]
    filterset_fields = ["is_paid", "created_at"]
    ordering_fields = ["-created_at"]


    def get_queryset(self):
        return Invoice.objects.filter(client=self.request.user).order_by("-created_at")
    




class DetailPaymentView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)




class DetailInvoiceView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    lookup_field = 'slug' 

    def get_queryset(self):
        return Invoice.objects.select_related('client').filter(client=self.request.user)
    


class DetailTransactionView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Invoice.objects.filter(client=self.request.user)




