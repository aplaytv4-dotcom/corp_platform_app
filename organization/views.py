from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from organization.models import Department, Management
from organization.permissions import IsAdmin
from organization.selectors import get_departments_for_user, get_managements_for_user
from organization.serializers import (
    DepartmentCreateSerializer,
    DepartmentListSerializer,
    DepartmentUpdateSerializer,
    ManagementCreateSerializer,
    ManagementListSerializer,
    ManagementUpdateSerializer,
)


class ManagementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        return get_managements_for_user(self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ManagementCreateSerializer
        if self.action in {"update", "partial_update"}:
            return ManagementUpdateSerializer
        return ManagementListSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        return get_departments_for_user(self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return DepartmentCreateSerializer
        if self.action in {"update", "partial_update"}:
            return DepartmentUpdateSerializer
        return DepartmentListSerializer
