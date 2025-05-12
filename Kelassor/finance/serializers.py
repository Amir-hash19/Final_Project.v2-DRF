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



