from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .tasks import send_welcome_sms_task




@receiver(post_save, sender=CustomUser)
def send_welcome_message(sender, created, instance, **kwargs):
    if created:
        last_name = instance.last_name
        user_phone_number = instance.phone

        
        send_welcome_sms_task.delay(last_name, user_phone_number)
        

