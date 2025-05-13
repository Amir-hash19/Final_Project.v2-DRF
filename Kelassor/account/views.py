from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .OTPThrottle import OTPThrottle
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group
from .models import CustomUser, AdminActivityLog
from .serializers import (CreateAccountSerializer, EditAccountSerializer, CustomAccountSerializer,
                           SupportPanelSerializer, OTPSerializer, VerifyOTPSerializer, PromoteUserSerializer, 
                           GroupSerializer, AdminActivityLogSerializer)
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import GroupPermission, is_supportpanel_user
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils.timezone import now, timedelta
from rest_framework import status
from django.db import transaction
from .OTPThrottle import OTPThrottle
from .tasks import send_otp_task
from django.core.cache import cache
import json

class CustomPagination(PageNumberPagination):
    page_size = 20



class CreateGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def perform_create(self, serializer):
        serializer.save()



#ساختن اکانت عادی برای کاربر نرمال 
class RegisterAccountView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            serializer = CreateAccountSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                refresh = RefreshToken.for_user(user)

                return Response({
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                    },status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#ویرایش اکانت برای کاربر عادی
class EditAccountView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditAccountSerializer

    def get_object(self):
        return self.request.user
    


#برای خروج کاربر
class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()

            # ثبت لاگ اگر کاربر عضو supportpanel بود
            user = request.user
            if is_supportpanel_user(user):
                AdminActivityLog.objects.create(
                    user=user,
                    action="Logout",
                    detail="User manually logged out",
                    ip_address=request.META.get("REMOTE_ADDR"),
                    user_agent=request.META.get("HTTP_USER_AGENT")
                )

            return Response({"detail": "User Logged Out Successfully!"})
        except Exception as e:
            return Response({"detail": "Error during logout, please try again later."}, status=500)






class DeleteAccountView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomAccountSerializer

    def get_object(self):
        return self.request.user
    



class DetailAccountView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomAccountSerializer


    def get_object(self):
        return self.request.user
    




class ListSupportAccountView(ListAPIView):
    queryset = CustomUser.objects.filter(groups__name__in=["SupportPanel"])
    permission_classes = [IsAuthenticated,GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = SupportPanelSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["date_joined", "phone", "username", "last_name"]
    filterset_fields = ["date_joined", "birthday"]
    ordering_fields = ["-date_joined"]





class SendOTPLogInView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = OTPSerializer(data=request.data) 

        if serializer.is_valid():
            phone = str(serializer.validated_data["phone"]) 


            send_otp_task.delay(phone)


            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






MAX_FAILED_ATTEMPTS = 5
BLOCK_TIME_SECONDS = 300  

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = str(serializer.validated_data["phone"])
            otp = serializer.validated_data["otp"]

            fail_key = f"otp_fail:{phone}"
            blocked = cache.get(fail_key)

            if blocked and int(blocked) >= MAX_FAILED_ATTEMPTS:
                return Response({"error": "Too many attempts. Please try again later."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)

            cached_otp = cache.get(f"otp:{phone}")
            if cached_otp and str(cached_otp) == otp:
                cache.delete(f"otp:{phone}")  
                cache.delete(fail_key)  

             
                user = get_user_model().objects.filter(phone=phone).first()
                if not user:
                    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

                refresh = RefreshToken.for_user(user)

                if is_supportpanel_user(user):
                    AdminActivityLog.objects.create(
                        admin_user=user,
                        action="Login via OTP",
                        detail="User Successfully logged in using OTP",
                        ip_address=request.META.get("REMOTE_ADDR"),
                        user_agent=request.META.get("HTTP_USER_AGENT")

                    )

                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                })

            else:
                # افزایش شمارنده تلاش ناموفق
                current_fails = cache.get(fail_key, 0)
                cache.set(fail_key, int(current_fails) + 1, timeout=BLOCK_TIME_SECONDS)

                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class PromoteUserView(APIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]

    
    def post(self, request):
        serializer = PromoteUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
           
            
            try:
                user = CustomUser.objects.get(email__iexact=email)
            except CustomUser.DoesNotExist:
                return Response({"detail": "email does not exis!"}, status=status.HTTP_404_NOT_FOUND)
            
            if user.is_superuser:
                return Response({"detail":"This User Already is SuperUser!"})

            user.is_superuser = True
            user.is_staff = True
            user.save()

            group, _ = Group.objects.get_or_create(name='SupportPanel')
            user.groups.add(group)

            return Response({
                "detail": f"Client {user.email} has been promoted successfully."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        



class DeleteSupportPanelView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]
    serializer_class = SupportPanelSerializer


    def perform_destroy(self, instance):
        if self.request.user == instance:
            raise ValidationError("You Cannot Delete your own account from here!")
        

class AdminLogOutView(APIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"details":"User Logged Out Successfully!"})
        except Exception as e:
            return Response({"details": "Error during logout, please try again later."}, status=500)






class ListAdminActivityLogView(ListAPIView):
    serializer_class = AdminActivityLogSerializer
    permission_classes = [IsAuthenticated, GroupPermission("SupperUser")]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["action", "detail", "user__username", "user__phone"]
    filterset_fields = ["created_at"]
    ordering_fields = ["-created_at"]



    def get_queryset(self):
        last_72_hours = now() - timedelta(hours=72)

        return AdminActivityLog.objects.filter(
            user__groups__name="SupportPanel",
            created_at__gte=last_72_hours
        )