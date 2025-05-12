from django.urls import path, include
from .views import CreateTickectView, DeleteTicketView, ListTicketView
from rest_framework.routers import DefaultRouter
from .views import  ListTickectViewSet


router = DefaultRouter()
router.register(r"tickets", ListTickectViewSet, basename='ticket')



urlpatterns = [
    path("add-ticket/", CreateTickectView.as_view(), name="create-tickect"),
    path("delete-ticket/<slug:slug>/", DeleteTicketView.as_view(), name="delete-ticket"),
    path("list-tickets/", ListTicketView.as_view(), name="list-tickets"),
    
    path("", include(router.urls)),
]
