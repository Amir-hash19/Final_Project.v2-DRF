from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from account.permissions import GroupPermission
from account.views import CustomPagination
from rest_framework import viewsets
from .models import BootcampCategory, Bootcamp, BootcampRegistration, SMSLog
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import (BootcampSerializer,CategoryBootcampSerializer, BootcampCountSerializer,BootcampCategorySerializer,BootcampRegistrationCreateSerializer,
                                        AdminBootcampRegistrationSerializer, BootCampRegitrationSerializer, BootcampStudentSerializer,
                                        SMSLogSerializer, MassNotificationSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from django.db.models import Count
from django.utils import timezone
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
    queryset = Bootcamp.objects.filter(status="registering").order_by("-created_at")
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
    queryset = BootcampRegistration.objects.filter(status='pending').order_by("-registered_at")
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootCampRegitrationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["phone_number", "comment"]
    filterset_fields = ["payment_type", "status", "reviewed_by"]
    ordering_fields = ["-registered_at"]
    






class CheckRegistraionStatusView(UpdateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    queryset = BootcampRegistration.objects.all()
    serializer_class = AdminBootcampRegistrationSerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        serializer.save(
            reviewed_by=self.request.user, reviewed_at=timezone.now()
        )
        



class CreateBootcampRegistrationView(CreateAPIView):
    queryset = BootcampRegistration.objects.all()
    serializer_class = BootcampRegistrationCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            volunteer=self.request.user
        )





class BootcampApprovedStudentsListView(ListAPIView):#لیست اعضای یه بوت کمپ
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootcampStudentSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        try:
            bootcamp = Bootcamp.objects.get(slug=slug)
        except Bootcamp.DoesNotExist:
            raise NotFound("BootCamp does Not existed!") 
        
        return BootcampRegistration.objects.filter(bootcamp=bootcamp, status='approved')   






class ListSMSLogView(ListAPIView):
    queryset = SMSLog.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]
    serializer_class = SMSLogSerializer



class DeleteSMSLogView(DestroyAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]
    queryset = SMSLog.objects.all()
    serializer_class = SMSLogSerializer




class MassNotificationView(APIView):
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]



    def post(self, request):
        serializer = MassNotificationSerializer(data=request.data)
        if serializer.is_valid():
            notifications = serializer.save()
            return Response({
                "detail": f"{len(notifications)} notifications created and are being sent."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)