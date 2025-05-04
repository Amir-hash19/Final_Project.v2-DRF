from django.urls import path
from .views import CreateAccountUserView, EditAccountView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("create-account/", CreateAccountUserView.as_view(), name="create-account"),
    path("edit-account/", EditAccountView.as_view(), name="edit-account"),
    path("refresh-token/", TokenRefreshView.as_view())

]    
