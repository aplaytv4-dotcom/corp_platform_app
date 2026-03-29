from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/auth/", include("accounts.auth_urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("organization.urls")),
    path("api/", include("staff.urls")),
    path("api/", include("attendance.urls")),
    path("api/", include("common.urls")),
]
