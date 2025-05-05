from django.urls import path
from .views import AdminCreateBootcampView, AdminCreateCategoryView, AdminEditCategoryView



urlpatterns = [
    path("add-bootcamp/", AdminCreateBootcampView.as_view(), name="create-bootcamp-by-admin"),
    path("add-category/", AdminCreateCategoryView.as_view(), name="create-category-by-admin"),
    path("edit-category/<slug:slug>/", AdminEditCategoryView.as_view(), name="edit-bootcamp-by-admin"),

]
