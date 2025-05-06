from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .OTPThrottle import OTPThrottle
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group
from .models import CustomUser
from .serializers import (CreateAccountSerializer, EditAccountSerializer, CustomAccountSerializer,
                           SupportPanelSerializer, OTPSerializer, VerifyOTPSerializer, PromoteUserSerializer)
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import GroupPermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.db import transaction
from .OTPThrottle import OTPThrottle
from .tasks import send_otp_task
from django.core.cache import cache
import json

class CustomPagination(PageNumberPagination):
    page_size = 20



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
        # request.user.auth_token.delete()
        return Response({"details":"User Logged Out Successfully!"})
    



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
        


class LogOutAdminView(APIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]

    def post(self, request):
        # request.user.auth_token.delete()
        return Response({"details":"User Logged Out Successfully!"})