from django.urls import include, path
from rest_framework.routers import DefaultRouter

from organization.views import DepartmentViewSet, ManagementViewSet


router = DefaultRouter()
router.register("managements", ManagementViewSet, basename="managements")
router.register("departments", DepartmentViewSet, basename="departments")


urlpatterns = [
    path("", include(router.urls)),
]
