from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from applications import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.frontend_page, {"page": "index.html"}, name="home"),
    path("apply.html", views.frontend_page, {"page": "apply.html"}, name="apply"),
    path("status.html", views.frontend_page, {"page": "status.html"}, name="status"),
    path("styles.css", serve, {"document_root": settings.FRONTEND_DIR, "path": "styles.css"}),
    path("script.js", serve, {"document_root": settings.FRONTEND_DIR, "path": "script.js"}),
    path("config.js", serve, {"document_root": settings.FRONTEND_DIR, "path": "config.js"}),
    re_path(
        r"^assets/(?P<path>.*)$",
        serve,
        {"document_root": settings.FRONTEND_DIR / "assets"},
    ),
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
