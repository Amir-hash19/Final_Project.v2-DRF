from rest_framework.serializers import ModelSerializer
from .models import Invoice, Transaction, Payment
from rest_framework import serializers
from account.models import CustomUser
from django.db import transaction




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




class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["slug", "user", "invoice"]

    def validate_invoice(self, invoice):
        request = self.context["request"]
        user = request.user


        if invoice.client != user:
            raise serializers.ValidationError("You have to choose your invoices!")
        return invoice
    
    def validate(self, data):
        method = data.get("method")
        tracking_code = data.get("tracking_code")
        receipt_image = data.get("receipt_image")


        if method == "offline" and (not tracking_code or not receipt_image):
            raise serializers.ValidationError("Please upload your picture and tracking code")
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            validated_data["user"] = self.context["request"].user
            return super().create(validated_data)    



