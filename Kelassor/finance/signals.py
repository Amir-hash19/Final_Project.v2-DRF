from django.db.models.signals import pre_save
from .models import Invoice, Payment, Transaction
from django.utils.text import slugify
from django.dispatch import receiver
from datetime import datetime
import uuid

@receiver(pre_save, sender=Invoice)
def generate_invoice_slug(sender, instance, **kwargs):
    if not instance.slug:
        date_part = datetime.now().strftime('%Y%m%d')
        uuid_part = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"invoice-{date_part}-{uuid_part}")
