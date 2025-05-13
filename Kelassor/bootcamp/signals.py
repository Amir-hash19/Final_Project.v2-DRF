from django.db.models.signals import post_save, pre_save
from .models import BootcampRegistration, Bootcamp, BootcampCategory
from django.dispatch import receiver
from django.utils.text import slugify
from .tasks import send_sms_to_user
from django.db.models import F
from datetime import datetime
import uuid




@receiver(post_save, sender=Bootcamp)
def generate_slug_bootcamp(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"{base_slug}-{unique_suffix}")




@receiver(post_save, sender=BootcampRegistration)
def generate_slug_registration(sender, instance, **kwargs):
    if not instance.slug:
        date_part = datetime.now().strftime("%Y%m%d")
        uuid_part = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"b-registration-{date_part}-{uuid_part}")




@receiver(post_save, sender=BootcampCategory)
def generate_slug_category(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"{base_slug}-{unique_suffix}")




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





