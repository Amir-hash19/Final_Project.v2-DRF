from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (TicketSerializer ,TicketMessageCreateSerializer, TicketMessageSerializer, 
                                            AdminEditableTicketMessageSerializer, TicketMessageCreateSerializer)
from account.permissions import GroupPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Ticket, TicketMessage
from account.views import CustomPagination
from rest_framework.exceptions import ValidationError
from rest_framework import status, serializers
from rest_framework.response import Response
from django.db import transaction
from django.db import transaction
from rest_framework.exceptions import NotFound
from bootcamp.models import Bootcamp, BootcampRegistration
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend





class CreateTickectView(CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]



class DeleteTicketView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    
    def get_object(self):
        return self.request.user



class ListTicketView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "slug"]
    filterset_fields = ["created_at", "status"]
    ordering_fields = ["-created_at"]
    def get_queryset(self):   
        return Ticket.objects.filter(user=self.request.user)
    
        



class EditTicketView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

        


class CreateTicketMessageView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketMessageSerializer
    
    def perform_create(self, serializer):
        ticket_slug = self.kwargs.get('slug')

        try:
            ticket = Ticket.objects.get(slug=ticket_slug)
        except Ticket.DoesNotExist:
            raise NotFound("Ticket not found!")

        if ticket.user != self.request.user:
            raise NotFound("You can only choose your ticket")

        serializer.save(ticket=ticket)




class ListTicketMessageView(ListAPIView):
    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageCreateSerializer
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["message", "title"]
    filterset_fields = ["created_at", "message_status"]
    ordering_fields = ["-created_at"]
    



        

class AdminResponseMessageView(UpdateAPIView):
    queryset = TicketMessage.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    serializer_class = AdminEditableTicketMessageSerializer
    lookup_field = 'slug'


        



class AdminDetailMessageView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, GroupPermission("SupportPanel", "SuperUser")]
    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageSerializer
    lookup_field = 'slug'