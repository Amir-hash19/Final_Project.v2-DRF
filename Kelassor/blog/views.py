from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.permissions import GroupPermission
from rest_framework.views import APIView
from .serializers import BlogCategorySerializer, UploadBlogSerializer
from .models import CategoryBlog, Blog








#اضافه کردن دسته بندی توسط سوپریوزر و پنل ادمین
class AddCategoryBlogView(CreateAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]
    serializer_class = BlogCategorySerializer







class UploadBlogView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = UploadBlogSerializer
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]

    def perform_create(self, serializer):
        serializer.save(
            user = self.request.user
        )