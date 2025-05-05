from django.urls import path
from .views import (AdminCreateBootcampView, AdminCreateCategoryView, AdminEditCategoryView,
                     AdminDeleteCategoryView, AdminEditBootCampView, AdminDeleteBootCampView, ListAvailableBootCamp, ListCategoryBootcampView, AdminListAllBootCampView)




urlpatterns = [
    path("add-bootcamp/", AdminCreateBootcampView.as_view(), name="create-bootcamp-by-admin"),
    path("add-category/", AdminCreateCategoryView.as_view(), name="create-category-by-admin"),
    path("edit-category/<slug:slug>/", AdminEditCategoryView.as_view(), name="edit-bootcamp-by-admin"),
    path("delete-bootcamp-category/<slug:slug>/", AdminDeleteCategoryView.as_view(), name="delete-bootcamp-category-by-superuser"),
    #از این به پایین تست نشده در پستمن
    path("edit-bootcamp/<slug:slug>/", AdminEditBootCampView.as_view(), name="edit-bootcamp-by-admin"),
    path("delete-bootcamp/<slug:slug>/", AdminDeleteBootCampView.as_view(), name="delete-bootcamp-by-admin"),
    path("list-bootcamps/", ListAvailableBootCamp.as_view(), name="list-registering-bootcamps"),
    path("list-category-bootcamp/", ListCategoryBootcampView.as_view(), name="list-bootcamp-category"),
    path("list-all-bootcamps/", AdminListAllBootCampView.as_view(), name="list-all-bootcamps-for-admin")


]
