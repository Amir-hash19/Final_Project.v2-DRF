from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .OTPThrottle import OTPThrottle
from .models import CustomUser
from .serializers import CreateAccountSerializer
from rest_framework.views import APIView
from .permissions import GroupPermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status




class CreateAccountUserView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "user":serializer.data,
                "refresh":str(refresh),
                "access":str(refresh.access_token)
                },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




            
       