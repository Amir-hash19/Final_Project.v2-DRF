from django.urls import path
from .views import AddCategoryBlogView, UploadBlogView



urlpatterns = [
    path("add-category/", AddCategoryBlogView.as_view(), name="create-category-blog"),
    path("upload-blog/", UploadBlogView.as_view(), name="create-blog"),
]
