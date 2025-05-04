from django.urls import path
from .views import AddCategoryBlogView, UploadBlogView, DeleteCategoryBlogView



urlpatterns = [
    path("add-category/", AddCategoryBlogView.as_view(), name="create-category-blog"),
    path("upload-blog/", UploadBlogView.as_view(), name="create-blog"),
    path("delete-category/<int:pk>", DeleteCategoryBlogView.as_view(), name="delete-category-blog")
]
