from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group 
from rest_framework.test import APITestCase
from django.utils.text import slugify
from account.models import CustomUser 
from .models import Invoice, Payment
from datetime import date, timedelta 
from rest_framework import status
from django.urls import reverse
import uuid 



User = get_user_model()

class CreateInvoiceViewAPITest(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(
            username="testalireza@1", email="testalireza1@email.com",
            national_id="1987987864", phone="+989051066658", slug="test-alireza"
        )
        self.superuser=User.objects.create_user(
            username="testadmin@22", email="testadmin22@email.com",
            national_id="1987987863", phone="+989051566658", slug="test-admin"
        )
        superuser_group = Group.objects.create(name="SuperUser")
        self.superuser.groups.add(superuser_group)

        self.url = reverse("create-invoice-for-user-by-admin")

        self.valid_payload = {
            "client": self.user.username,
            "amount": "1234.567",
            "deadline": (date.today() + timedelta(days=30)).isoformat(),
            "description": "Test invoice",
            "slug":slugify("testalireza") + "-" +str(uuid.uuid4())[:8]
        }

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


    def test_create_invoice_unauthenticated(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def authorize_client_as(self, user):
        token = self.get_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")



    def test_create_invoice_without_permission(self):
        self.authorize_client_as(self.user)
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_create_invoice_with_permission(self):
        self.authorize_client_as(self.superuser)
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Invoice.objects.filter(client=self.user).exists())



    def test_create_invoice_invalid_amount(self):
        self.authorize_client_as(self.superuser)
        invalid_payload = self.valid_payload.copy()
        invalid_payload["amount"] = "not-a-number"
        response = self.client.post(self.url, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



