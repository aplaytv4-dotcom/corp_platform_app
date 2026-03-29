from django.urls import include, path
from rest_framework.routers import DefaultRouter

from staff.views import AssignmentViewSet, EmployeeViewSet, PositionViewSet, StaffUnitViewSet


router = DefaultRouter()
router.register("positions", PositionViewSet, basename="positions")
router.register("staff-units", StaffUnitViewSet, basename="staff-units")
router.register("employees", EmployeeViewSet, basename="employees")
router.register("assignments", AssignmentViewSet, basename="assignments")


urlpatterns = [
    path("", include(router.urls)),
]
