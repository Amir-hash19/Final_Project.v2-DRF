from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

User = get_user_model()


class PromoteUserViewTests(APITestCase):
    def setUp(self):
        # کاربر پروموتر که قراره بقیه رو ارتقا بده
        self.promoter = User.objects.create_user(
            username='adminuser',
            email='admin1@email.com',
            phone='+989121234567',
            national_id='3333333333',
            slug='admin1-user'
        )

        # گروهی که دسترسی داره
        group, _ = Group.objects.get_or_create(name='SuperUser')
        self.promoter.groups.add(group)

        # کاربری که قراره پروموت بشه
        self.target_user = User.objects.create_user(
            username='targetuser',
            email='target1@email.com',
            phone='+989121234568',
            national_id='2222222222',
            slug='target1-user'
        )

        self.url = reverse('promote-user')  # باید این نام در urls تعریف شده باشه
        self.client.force_authenticate(user=self.promoter)

    def test_promote_to_supportpanel(self):
        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "SupportPanel"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.target_user.groups.filter(name="SupportPanel").exists())

    def test_promote_to_superuser(self):
        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "SuperUser"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.target_user.groups.filter(name="SuperUser").exists())

    def test_user_already_superuser(self):
        self.target_user.is_superuser = True
        self.target_user.save()

        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "SuperUser"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_promote_user_does_not_exist(self):
        response = self.client.post(self.url, {
            "email": "notfound@example.com",
            "group_name": "SupportPanel"
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_group_name(self):
        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "InvalidGroup"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_without_permission(self):
        self.client.logout()

        normal_user = User.objects.create_user(
            username='normal',
            email='normal1@email.com',
            phone='+989121234569',
            national_id='4444444444',
            slug='normal1-user'
        )

        self.client.force_authenticate(user=normal_user)

        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "SupportPanel"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
