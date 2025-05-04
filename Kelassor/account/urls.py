from django.urls import path
from .views import CreateAccountUserView


urlpatterns = [
    path("create-account/", CreateAccountUserView.as_view(), name="create-account")
]
