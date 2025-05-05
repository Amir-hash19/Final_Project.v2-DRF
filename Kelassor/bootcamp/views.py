from rest_framework.generics import CreateAPIView, ListAPIView
from account.permissions import GroupPermission
from account.views import CustomPagination
from .models import BootcampCategory, Bootcamp, BootcampRegistration
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import BootcampSerializer, CategoryBootcampSerializer




class AdminCreateBootcampView(CreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = BootcampSerializer
    queryset = Bootcamp.objects.all()




class AdminCreateCategoryView(CreateAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = CategoryBootcampSerializer
    queryset = BootcampCategory.objects.all()


