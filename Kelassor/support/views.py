from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import TicketSerializer, TicketCreateSerializer, TicketMessageSerializer, AdminTicketMessageResponseSerializer
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
    
        












class ListTickectViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "title"]
    filterset_fields = ["created_at"]
    ordering_fields = ["-created_at"]
    



        




        



