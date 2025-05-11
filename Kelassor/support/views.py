from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import TickectSerializer, TicketCreateSerializer, TicketMessageSerializer, AdminTicketMessageResponseSerializer
from account.permissions import GroupPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Ticket, TicketMessage
from account.views import CustomPagination
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from bootcamp.models import Bootcamp, BootcampRegistration
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend





class CreateTickectView(CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TickectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        bootcamp_title = self.request.data.get('bootcamp_title') 

        registrations = BootcampRegistration.objects.filter(bootcamp=bootcamp, status='pending')

        try:
            bootcamp = Bootcamp.objects.get(title=bootcamp_title)
        except Bootcamp.DoesNotExist:
            return Response({"detail":"BootCamp not found"}, status=status.HTTP_404_NOT_FOUND)    
        
        if not registrations:
            return Response({"detail": "No registrations are in pending status for this bootcamp."},
                           status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            serializer.save(
                user=self.request.user, bootcamp=bootcamp
            )
                            

        





class ListTickectViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "title"]
    filterset_fields = ["created_at"]
    ordering_fields = ["-created_at"]
    



        


class CreateMessageTicketView(CreateAPIView):
    queryset = TicketMessage.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TicketMessageSerializer  

    def perform_create(self, serializer):
            
            title = self.request.data.get('title')
            if not title:
                raise ValidationError({"title":"this fields is required"})
            
            ticket = get_object_or_404(Ticket, title=title, user=self.request.user)

            with transaction.atomic():
                serializer.save(
                    sender=self.request.user,
                    ticket=ticket
                )




        
    
class ListTicketMessageView(ListAPIView):
    serializer_class = TicketMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TicketMessage.objects.select_related('ticket')
        if user.groups.filter(name__in=["SupportPanel", "SuperUser"]).exists():
            return TicketMessage.objects.all()
        return TicketMessage.objects.filter(ticket__user=user)
    




class AdminRespondToTicketMessageView(UpdateAPIView):
    queryset = TicketMessage.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = AdminTicketMessageResponseSerializer


    def perform_update(self, serializer):
        serializer.save(admin=self.request.user)
        