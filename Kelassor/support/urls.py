from django.urls import path, include
from .views import CreateTickectView, CreateMessageTicketView
from rest_framework.routers import DefaultRouter
from .views import CreateTickectViewSet, ListTickectViewSet


router = DefaultRouter()
router.register(r"tickets", ListTickectViewSet, basename='ticket')



urlpatterns = [
    path("add-tickect/", CreateTickectView.as_view(), name="create-tickect"),
    path("ticket/message/create/", CreateMessageTicketView.as_view(), name="create-ticket-message"),
    path("", include(router.urls)),
]
