from django.urls import path, include
from .views import CreateTickectView, CreateMessageTicketView, ListTicketMessageView, AdminRespondToTicketMessageView, DeleteTicketView
from rest_framework.routers import DefaultRouter
from .views import  ListTickectViewSet


router = DefaultRouter()
router.register(r"tickets", ListTickectViewSet, basename='ticket')



urlpatterns = [
    path("add-ticket/", CreateTickectView.as_view(), name="create-tickect"),
    path("delete-ticket/<slug:slug>/", DeleteTicketView.as_view(), name="delete-ticket"),

    path("ticket/message/create/", CreateMessageTicketView.as_view(), name="create-ticket-message"),
    path("list-ticket-messages/", ListTicketMessageView.as_view(), name="ticket-message-view"),
    path("response-to-messages/<slug:slug>/", AdminRespondToTicketMessageView.as_view(), name="response-to-ticket"),
    path("", include(router.urls)),
]
