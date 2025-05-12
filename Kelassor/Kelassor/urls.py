from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("account.urls")),
    path("blogs/", include("blog.urls")),
    path("bootcamps/", include("bootcamp.urls")),
    path("support/", include("support.urls")),
    path("finance/", include("finance.urls")),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)