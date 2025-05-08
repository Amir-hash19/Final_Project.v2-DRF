from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework import viewsets
from account.permissions import GroupPermission
from account.views import CustomPagination
from .models import BootcampCategory, Bootcamp, BootcampRegistration
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import (BootcampSerializer,CategoryBootcampSerializer, BootcampCountSerializer,BootcampCategorySerializer,BootcampRegistrationSerializer,
                                        BootCampRegistraionSerializer, BootCampRegitrationSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from django.db.models import Count
from django.http import Http404




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





class ListAvailableBootCampViewSet(viewsets.ModelViewSet):
    queryset = Bootcamp.objects.filter(status="registering")
    permission_classes = [AllowAny]
    serializer_class = BootcampSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "category", "created_at"]
    filterset_fields = ["is_online", "price"]
    ordering_fields = ["-created_at"]
    lookup_field = 'slug'



class BootcampCategoryViewSet(viewsets.ModelViewSet):
    queryset = BootcampCategory.objects.all()
    serializer_class = BootcampCategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'





class ListCategoryBootcampView(ListAPIView):
    queryset = BootcampCategory.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
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




class DetailBootCampView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BootcampSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Bootcamp.objects.filter(status="registering")
     
    def get_object(self):
        try:
            return super().get_object()    
        except Http404:
            raise NotFound("Bootcamp nor found !")






class MostRequestedBootCampView(ListAPIView):
    serializer_class = BootcampCountSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return 
    Bootcamp.objects.annotate(
        request_count=Count("registrations")
    ).order_by("-request_count")[:10]






class ListBootCampRegistrationView(ListAPIView):
    queryset = BootcampRegistration.objects.filter(status='pending')
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampRegitrationSerializer






class CreateBootcampRegistrationView(CreateAPIView):
    serializer_class = BootcampRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BootcampRegistration.objects.filter(volunteer=self.request.user)


    def perform_create(self, serializer):
        user = self.request.user
        bootcamp = serializer.validated_data['bootcamp']


        if bootcamp.status != 'registering':
            raise ValidationError("this bootcamp is not available!")


        previous = BootcampRegistration.objects.filter(
            volunteer = user,
            status = "approved"
        ).order_by("-registered_at").filter()

        if previous:
            serializer.validated_data["phone_number"] = previous.phone_number
            serializer.validated_data["payment_type"] = previous.payment_type
            serializer.validated_data['slug'] = f"{bootcamp.slug}-{user.id}"
            
        serializer.save(volunteer=user)    





class CheckRegistraionStatusView(UpdateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    queryset = BootcampRegistration.objects.all()
    serializer_class = BootCampRegistraionSerializer

    def perform_update(self, serializer):
        reviewed_by = self.request.user

        