from django.urls import path
from .views import AdminCreateBootcampView, AdminCreateCategoryView



urlpatterns = [
    path("add-bootcamp/", AdminCreateBootcampView.as_view(), name="create-bootcamp-by-admin"),
    path("add-category/", AdminCreateCategoryView.as_view(), name="create-category-by-admin"),
    
]
