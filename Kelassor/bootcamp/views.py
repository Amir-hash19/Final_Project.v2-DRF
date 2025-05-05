from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from account.permissions import GroupPermission
from account.views import CustomPagination
from .models import BootcampCategory, Bootcamp, BootcampRegistration
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import BootcampSerializer, CategoryBootcampSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



class AdminCreateBootcampView(CreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootcampSerializer
    queryset = Bootcamp.objects.all()




class AdminCreateCategoryView(CreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = CategoryBootcampSerializer
    queryset = BootcampCategory.objects.all()
    



class AdminEditCategoryView(UpdateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = CategoryBootcampSerializer
    queryset = BootcampCategory.objects.all()
    lookup_field = 'slug'
    



class AdminDeleteCategoryView(DestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]
    serializer_class = CategoryBootcampSerializer
    queryset = BootcampCategory.objects.all()
    lookup_field = 'slug'





class AdminEditBootCampView(UpdateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel","SuperUser")]
    serializer_class = BootcampSerializer
    queryset = Bootcamp.objects.all()
    lookup_field = 'slug'





class AdminDeleteBootCampView(DestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel","SuperUser")]
    serializer_class = BootcampSerializer
    queryset = Bootcamp.objects.all()
    lookup_field = 'slug'





class ListAvailableBootCamp(ListAPIView):
    queryset = Bootcamp.objects.filter(status="registering")
    permission_classes = [IsAuthenticated]
    serializer_class = BootcampSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "category", "created_at"]
    filterset_fields = ["is_online", "price"]
    ordering_fields = ["-created_at"]





class ListCategoryBootcampView(ListAPIView):
    queryset = BootcampCategory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryBootcampSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    filterset_fields = ["date_created"]
    ordering_fields = ["-date_created"]






class AdminListAllBootCampView(ListAPIView):
    queryset = Bootcamp.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootcampSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    filterset_fields = ["status", "is_online", "category", "created_at"]
    ordering_fields = ["-created_at"]







