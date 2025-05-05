from django.urls import path
from .views import AdminCreateBootcampView



urlpatterns = [
    path("add-bootcamp/", AdminCreateBootcampView.as_view(), name="create-bootcamp-by-admin"),
]
