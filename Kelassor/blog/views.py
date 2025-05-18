from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.permissions import GroupPermission, GroupHasDynamicPermission
from rest_framework.views import APIView
from .serializers import BlogCategorySerializer, UploadBlogSerializer, BlogSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from rest_framework.response import Response
from .models import CategoryBlog, Blog
from account.views import CustomPagination
from .filters import CategoryBlogFilter







#اضافه کردن دسته بندی توسط سوپریوزر و پنل ادمین
class AddCategoryBlogView(CreateAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]
    serializer_class = BlogCategorySerializer





class UploadBlogView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = UploadBlogSerializer
   

    def perform_create(self, serializer):
        serializer.save(
            uploaded_by = self.request.user
        )

    def get_permissions_classes(self):
        required_perms = ["blog.add_blog"]
        return [
            IsAuthenticated,
            GroupPermission("SuperUser", "SupportPanel"),
            lambda: GroupHasDynamicPermission(required_perms)
        ]    




class DeleteCategoryBlogView(DestroyAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BlogCategorySerializer






class ListCateogryBlogView(ListAPIView):
    queryset = CategoryBlog.objects.all().order_by("-date_created")
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BlogCategorySerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    filterset_class = CategoryBlogFilter

    



class EditBlogView(UploadBlogView):
    serializer_class = UploadBlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(uploaded_by=self.request.user)
    

    def get_permissions_classes(self):
        required_perms = ["blog.change_blog"]
        return [
            IsAuthenticated,
            GroupPermission("SuperUser", "SupportPanel"),
            lambda: GroupHasDynamicPermission(required_perms)
        ]
        







class DeleteBlogView(DestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = UploadBlogSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Blog.objects.filter(uploaded_by=self.request.user)
    





class DetailBlogView(RetrieveAPIView):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UploadBlogSerializer






class ListBlogView(ListAPIView):
    queryset = Blog.objects.filter(status="published")
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "status", "content"]
    filterset_fields = ["status", "date_added"]
    ordering_fields = ["-date_added"]






class AdminListBlogView(ListAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "status", "content"]
    filterset_fields = ["status", "date_added"]
    ordering_fields = ["-date_added"]





class BlogDownloadView(APIView):
    def get(self, request, slug, format=None):
        try:
            blog = Blog.objects.get(slug=slug)

            if blog.file and hasattr(blog.file, 'path'):
                file_path = blog.file.path
                response = FileResponse(open(file_path, 'rb'), as_attachment=True)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = f'attachment; filename="{blog.file.name}"'
                return response
            else:
                return Response({"detail": "No file available for this blog."}, status=404)

        except Blog.DoesNotExist:
            return Response({'detail': 'Blog not found.'}, status=404)
        except Exception as e:
            # اگر ارور دیگه‌ای پیش اومد، می‌تونی اینجا مدیریت کنی
            return Response({'detail': f'Error: {str(e)}'}, status=500)