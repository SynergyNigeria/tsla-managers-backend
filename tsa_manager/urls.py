from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from applications import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.api_home, name="api_home"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("api/applications", views.create_application, name="create_application"),
    path(
        "api/applications/<str:application_id>",
        views.application_status,
        name="application_status",
    ),
    path(
        "api/applications/<str:application_id>/capacity",
        views.update_car_capacity,
        name="update_car_capacity",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
