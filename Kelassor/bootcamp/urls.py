from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (AdminCreateBootcampView, AdminCreateCategoryView, AdminEditCategoryView,
                     AdminDeleteCategoryView, AdminEditBootCampView, AdminDeleteBootCampView, 
                     ListAvailableBootCamp, ListCategoryBootcampView, AdminListAllBootCampView,
                       DetailBootCampView, MostRequestedBootCampView, BootcampRegistrationViewSet)

router = DefaultRouter()
router.register(r'registrations', BootcampRegistrationViewSet)


urlpatterns = [
    path("add-bootcamp/", AdminCreateBootcampView.as_view(), name="create-bootcamp-by-admin"),
    path("add-category/", AdminCreateCategoryView.as_view(), name="create-category-by-admin"),
    path("edit-category/<slug:slug>/", AdminEditCategoryView.as_view(), name="edit-bootcamp-by-admin"),
    path("delete-bootcamp-category/<slug:slug>/", AdminDeleteCategoryView.as_view(), name="delete-bootcamp-category-by-superuser"),
    path("edit-bootcamp/<slug:slug>/", AdminEditBootCampView.as_view(), name="edit-bootcamp-by-admin"),
    path("delete-bootcamp/<slug:slug>/", AdminDeleteBootCampView.as_view(), name="delete-bootcamp-by-admin"),
    path("list-bootcamps/", ListAvailableBootCamp.as_view(), name="list-registering-bootcamps"),
    path("list-category-bootcamp/", ListCategoryBootcampView.as_view(), name="list-bootcamp-category"),
    path("list-all-bootcamps/", AdminListAllBootCampView.as_view(), name="list-all-bootcamps-for-admin"),
    path("detail-bootcamp/<slug:slug>/", DetailBootCampView.as_view(), name="detail-bootcamp"),
    path("most-registered-bootcamp", MostRequestedBootCampView.as_view(), name="list-most-registred-bootcamp"),
    path("", include(router.urls)),

]
