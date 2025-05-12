from .models import Payment, Invoice, Transaction
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from account.permissions import GroupPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status 
from account.views import CustomPagination
from rest_framework.exceptions import ValidationError
from account.models import CustomUser
from .serializers import InvoiceSerializer, BasicUserSerializer, PaymentSerializer
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
