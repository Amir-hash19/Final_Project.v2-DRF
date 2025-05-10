from django.db.models.signals import post_save, pre_save
from .models import BootcampRegistration
from django.dispatch import receiver
from .tasks import send_sms_to_user
from django.db.models import F



@receiver(post_save, sender=BootcampRegistration)
def check_capacity_bootcamp(sender, instance, created, **kwargs):
    if not created and instance.status == "approved":
        bootcamp = instance.bootcamp
        if bootcamp.capacity > 0:
            bootcamp.capacity -= 1
            bootcamp.save()







@receiver(pre_save, sender=BootcampRegistration)
def notify_user(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = BootcampRegistration.objects.get(id=instance.pk)
        except BootcampRegistration.DoesNotExist:
            previous = None    

        if previous and previous.status != instance.status:
            phone = str(instance.phone_number)
            full_name = str(instance.volunteer)

            send_sms_to_user.delay(phone, full_name)
