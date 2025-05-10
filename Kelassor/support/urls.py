from django.urls import path
from .views import CreateTickectView


urlpatterns = [
    path("add-tickect/", CreateTickectView.as_view(), name="create-tickect"),
]
