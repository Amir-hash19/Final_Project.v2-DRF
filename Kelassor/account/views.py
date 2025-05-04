from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .OTPThrottle import OTPThrottle
from .models import CustomUser
from .serializers import CreateAccountSerializer, EditAccountSerializer, CustomAccountSerializer, ListSupportPanelSerializer
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import GroupPermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status




class CustomPagination(PageNumberPagination):
    page_size = 20


#ساختن اکانت عادی برای کاربر نرمال 
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
    serializer_class = ListSupportPanelSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["date_joined", "phone", "username", "last_name"]
    filterset_fields = ["date_joined", "birthday"]
    ordering_fields = ["-date_joined"]