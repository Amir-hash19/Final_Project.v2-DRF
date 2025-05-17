from .models import Bootcamp, BootcampRegistration, BootcampCategory
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group 
from rest_framework.test import APITestCase
from django.utils.text import slugify
from account.models import CustomUser 
from datetime import date, timedelta ,datetime
from rest_framework import status
from django.urls import reverse
import datetime
import uuid 



User = get_user_model()




class AdminCreateBootcampViewTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin@%1", email="admintest1@email.com",
        national_id="8976756453", phone="+989966955432", slug="admin-test")

        self.regular_user = User.objects.create_user(username="user@%1", email="usertest1@email.com",
        national_id="8976758453", phone="+989966955433", slug="user-test")

        self.instructor1 = User.objects.create_user(username="teacher@%1", email="teachertest1@email.com",
        national_id="8976758653", phone="+989966951433", slug="teacher-test", last_name="testteacher")

        
        support_group = Group.objects.create(name="SupportPanel")
        self.admin_user.groups.add(support_group)
        self.admin_user.is_superuser = True
        self.admin_user.save()

        self.category = BootcampCategory.objects.create(name="AI Bootcamp", slug="ai")

        self.url = reverse("create-bootcamp-by-admin")


        self.payload = {
            "instructor": ["Instructor1"],  # چون slug_field='last_name' هست
            "title": "AI Bootcamp",
            "price": 1000,
            "capacity": 25,
            "category": self.category.pk,  # فیلد category دیگه url نیست پس pk بفرست
            "description": "Test bootcamp description",
            "start_date": "2025-06-01",
            "end_date": "2025-06-20",
            "hours": 40,
            "days": 10,
        }

    def get_token(self, user):
        return str(RefreshToken.for_user(user).access_token)
        


    def test_create_bootcamp_without_permission(self):
        token = self.get_token(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





class DetailBootCampViewTest(APITestCase):
    def setUp(self):
        self.category = BootcampCategory.objects.create(name="AI", slug="ai")
        self.bootcamp = Bootcamp.objects.create(
            title="AI Beginner",
            price=500,
            capacity=20,
            category=self.category,
            description="Desc",
            start_date=datetime.date(2025, 1, 1),
            end_date=datetime.date(2025, 2, 1),
            hours=40,
            days=20,
            slug="ai-beginner",
            status="registering",
            is_online=True,
        )
        self.url = reverse('detail-bootcamp', kwargs={'slug': self.bootcamp.slug})

    def test_get_existing_bootcamp(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.bootcamp.slug)

    def test_get_nonexistent_bootcamp_returns_404(self):
        url = reverse('detail-bootcamp', kwargs={'slug': 'non-existent-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Bootcamp nor found !")

    def test_get_bootcamp_with_wrong_status_returns_404(self):
        self.bootcamp.status = "closed"
        self.bootcamp.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Bootcamp nor found !")