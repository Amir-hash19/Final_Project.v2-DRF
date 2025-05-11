from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("account.urls")),
    path("blogs/", include("blog.urls")),
    path("bootcamps/", include("bootcamp.urls")),
    path("support/", include("support.urls")),
]
