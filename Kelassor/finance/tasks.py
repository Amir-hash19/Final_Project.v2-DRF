from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from kavenegar import KavenegarAPI
import os


api = KavenegarAPI(settings.KAVENEGAR_API_KEY)




@shared_task(bind=True, max_retries=3, default_retry_delay=60, ignore_result=True)  
def send_sms_for_invoice_task(self, phone_client, last_name):
    api_key = os.getenv('KAVENEGAR_API_KEY')  
    client = KavenegarAPI(api_key)
    cache_key = f"welcome_sms:{phone_client}"
    message = f"This message from kelassor, new invoice created for you please check your panel-->'https://kelaasor.com/'<--"

    try:
        params = {
            "receptor":phone_client,
            "sender":"2000660110",
            "message":message
        }
        response = client.sms_send(params)  
        return response
    except Exception as e:
        raise self.retry(exc=e)
    finally:
        cache.delete(cache_key)
    


