from .models import Payment, Invoice, Transaction
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from account.permissions import GroupPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status 
from account.views import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from account.views import CustomPagination
from rest_framework.exceptions import ValidationError
from account.models import CustomUser
from .serializers import InvoiceSerializer, BasicUserSerializer, PaymentSerializer, TransactionSerializer
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



class CreatePaymentView(CreateAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer


    def perform_create(self, serializer):
        invoice_slug = self.kwargs.get('slug')
        try:
            invoice = Invoice.objects.get(slug=invoice_slug)
        except Invoice.DoesNotExist:
            raise ValidationError({"invoice":"the invoice does not existed!"})


        if invoice.client != self.request.user:
            raise ValidationError("You can only select your invoice")
        

        serializer.save(user=self.request.user, invoice=invoice)




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
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    


class ListTransactionView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "amount"]
    filterset_fields = ["transaction_type", "transaction_date"]
    ordering_fields = ["-transaction_date"]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)