from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.permissions import GroupPermission
from rest_framework.views import APIView
from .serializers import BlogCategorySerializer, UploadBlogSerializer, BlogSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import CategoryBlog, Blog
from account.views import CustomPagination







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
            uploaded_by = self.request.user
        )




class DeleteCategoryBlogView(DestroyAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BlogCategorySerializer






class ListCateogryBlogView(ListAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BlogCategorySerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    filterset_fields = ["date_joined"]

    



class EditBlogView(UploadBlogView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = UploadBlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(uploaded_by=self.request.user)







class DeleteBlogView(DestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = UploadBlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)
    





class DetailBlogView(RetrieveAPIView):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UploadBlogSerializer






class ListBlogView(ListAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "status", "content"]
    filterset_fields = ["status", "date_added"]
    ordering_fields = ["-date_added"]