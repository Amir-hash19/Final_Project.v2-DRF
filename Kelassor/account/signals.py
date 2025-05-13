from django.db.models.signals import post_save
from django.utils.timezone import now
from .permissions import is_supportpanel_user
from django.dispatch import receiver
from .models import CustomUser
from .tasks import send_welcome_sms_task
from django.utils.text import slugify
from datetime import datetime
import uuid



@receiver(post_save, sender=CustomUser)
def send_welcome_message(sender, created, instance, **kwargs):
    if created:
        last_name = instance.last_name
        user_phone_number = str(instance.phone)

        
        send_welcome_sms_task.delay(last_name, user_phone_number)
        



@receiver(post_save, sender=CustomUser)
def generate_slug_customeuser(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.username)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"{base_slug}-{unique_suffix}")





