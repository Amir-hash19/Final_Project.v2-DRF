from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import TickectSerializer
from account.permissions import GroupPermission
from .models import Ticket, TicketMessage
from rest_framework import status




class CreateTickectView(CreateAPIView):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TickectSerializer

    def get_object(self):
        return self.request.user
