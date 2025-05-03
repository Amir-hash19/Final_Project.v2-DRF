from django.contrib import admin
from .models import Invoice, Payment ,Transaction , Wallet


admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Transaction)
admin.site.register(Wallet)
