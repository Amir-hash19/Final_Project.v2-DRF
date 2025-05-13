from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RegisterAccountView, EditAccountView, LogOutView, DeleteAccountView, DetailAccountView, 
                    ListSupportAccountView, ListAdminActivityLogView, SendOTPLogInView, VerifyOTPView, PromoteUserView, DeleteSupportPanelView, AdminLogOutView)
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CreateGroupViewSet

router = DefaultRouter()
router.register(r"groups", CreateGroupViewSet)
urlpatterns = [
    path("create-account/", RegisterAccountView.as_view(), name="create-account"),
    path("edit-account/", EditAccountView.as_view(), name="edit-account"),
    path("refresh-token/", TokenRefreshView.as_view()), #موقت فقط برای توکن گرفتن 
    path("logout-account/", LogOutView.as_view(), name="logging-Out"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
    path("detail-account/", DetailAccountView.as_view(), name="detail-account"),
    path("list-supportpanel-user/", ListSupportAccountView.as_view(), name="list-supportpanel-user"),
    path("loggin/", SendOTPLogInView.as_view(), name="send-otp"),
    path("verify-code/", VerifyOTPView.as_view(), name="verify-otp"),
    path("promote-to-superuser/", PromoteUserView.as_view(), name="change-to-superuser"),
    path("delete-supportpanel-user/<int:pk>/", DeleteSupportPanelView.as_view(), name="delete-supportpanel-user-by-superuser"),
    path("logout-admin/", AdminLogOutView.as_view(), name="logout-admin-view"),
    path("admin-activity-logs/", ListAdminActivityLogView.as_view(), name="admin-activity-logs"),
    path("", include(router.urls))

]    
