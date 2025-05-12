from django.db import models
from account.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid



class Invoice(models.Model):
    client = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    deadline = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return f"{self.amount}"
    



class Payment(models.Model):
    PAYMENT_METHODS = [
        ('online', 'Online Gateway'),
        ('offline', 'Offline Transfer')
    ]
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)


    def clean(self):
        super().clean()
        if self.method == "offline" and not self.tracking_code and not self.receipt_image:
            raise ValidationError("User must upload tracking code and receipt_images!")

    tracking_code = models.CharField(max_length=100, blank=True, null=True)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)


    def __str__(self):
        return self.method



class Transaction(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    is_verified = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.transaction_type}"
    













class Wallet(models.Model):
    class WalletStatus(models.TextChoices):
        ACTIVE = 'active', _('Active')
        BLOCKED = 'blocked', _('Blocked')
        SUSPENDED = 'suspended', _('Suspended')



    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='wallets')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    locked_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=WalletStatus.choices, default=WalletStatus.ACTIVE)
    last_transaction_at = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
       

    def __str__(self):
        return f"{self.user} -  {self.status}"
