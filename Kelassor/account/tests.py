from rest_framework.test import APITestCase, APIClient
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





class RegisterAccountViewTests(APITestCase):
    
    def test_register_user(self):
        url = reverse("create-account")
        data = {
            "username": "normaluser_@12",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "phone":'+989121234561',
            "email": "normal1212@email.com",
            "about_me": "Normaluser....",
            "national_id": "8888888888",
            "gender": "male"
        }

        response = self.client.post(url, data, format='json')
    

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["username"], "normaluser_@12")
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

        user = User.objects.get(username="normaluser_@12")
        self.assertEqual(user.groups.count(), 0)
       
    def test_register_user_cannot_groups(self):
        url = reverse("create-account")    

        data = {
            "username": "baduser@_22",
            "first_name": "Reza",
            "last_name": "Karimi",
            "phone": "+989961232542",
            "email": "reza2@email.com",
            "about_me": "",
            "national_id": "7777777777",
            "gender": "male",
            "group": "anything"
        }

        response = self.client.post(url , data, format="json")
          
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("group", response.data)
        self.assertEqual(str(response.data["group"][0]), "Group field should not be included in registration data.")
  
        