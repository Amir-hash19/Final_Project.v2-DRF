from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .serializers import UploadBlogSerializer
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from .models import Blog, CategoryBlog
from .views import UploadBlogView

User = get_user_model()


class UploadBlogViewTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory() 
       


        self.support_group=Group.objects.create(name="SupportPanel")
        self.superuser_group=Group.objects.create(name="SuperUser")


        self.user_with_permission = User.objects.create_user(username="permitted@12",
        password="pass1234", phone="+989917652134", email="permitted12@email.com", national_id="4444444444")
        self.user_with_permission.groups.add(self.support_group, self.superuser_group)



        self.user_without_permission = User.objects.create_user(username="noperm@12",
        password="pass1234", phone="+989213412564", email="noperm12@email.com", national_id="7685940328")

        self.category=CategoryBlog.objects.create(name="tech")

        
        self.valid_data = {
            "title":"test blog",
            "content":"this is test blog content",
            "blogcategory":self.category.id
        }

        self.data = self.valid_data
        self.url=reverse("create-blog")

    def test_upload_blog_with_force_authenticate(self):
        request = self.factory.post("/api/blogs/", self.data, format='json')
        force_authenticate(request, user=self.user_with_permission)
        view = UploadBlogView.as_view()


        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.first().uploaded_by, self.user_with_permission)