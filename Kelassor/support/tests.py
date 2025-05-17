from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from bootcamp.models import Bootcamp
from rest_framework import status
from django.urls import reverse
from .models import Ticket


User = get_user_model()



class CreateTicketAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testali@12", email="testali1@email.com"
            ,phone="+989122345431",national_id="9187435619", slug="test-ali"
        )
        self.url = reverse("create-tickect")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)


    def test_create_ticket_authenticated(self):

        data = {
            "title":"test ticket1",
            "description":"test description1",
        }    
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response=self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], 'test ticket1')
        self.assertEqual(response.data["user"], "testali@12")


    def test_create_ticket_unauthenticated(self):
        data = {
            "title":"test ticket2",
            "description":"test description2"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)