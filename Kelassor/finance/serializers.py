from rest_framework.serializers import ModelSerializer
from .models import Invoice, Transaction, Payment
from rest_framework import serializers
from account.models import CustomUser





class InvoiceSerializer(ModelSerializer):
    client = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all()
    )
    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ["slug"]



class BasicUserSerializer(serializers.ModelSerializer):
    invoice_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', "invoice_count"]