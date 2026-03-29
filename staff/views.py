from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from common.permissions import user_has_department_access
from staff.models import Employee, Position
from staff.permissions import IsAdmin
from staff.selectors import get_assignments_for_user, get_employees_for_user, get_staff_units_for_user
from staff.serializers import (
    CloseAssignmentSerializer,
    EmployeeAssignmentCreateSerializer,
    EmployeeAssignmentListSerializer,
    EmployeeAssignmentUpdateSerializer,
    EmployeeCreateSerializer,
    EmployeeListSerializer,
    EmployeeUpdateSerializer,
    PositionCreateSerializer,
    PositionListSerializer,
    PositionUpdateSerializer,
    StaffUnitCreateSerializer,
    StaffUnitListSerializer,
    StaffUnitUpdateSerializer,
    TransferEmployeeSerializer,
)
from staff.services import close_assignment


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return PositionCreateSerializer
        if self.action in {"update", "partial_update"}:
            return PositionUpdateSerializer
        return PositionListSerializer


class StaffUnitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_staff_units_for_user(self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return StaffUnitCreateSerializer
        if self.action in {"update", "partial_update"}:
            return StaffUnitUpdateSerializer
        return StaffUnitListSerializer

    def perform_create(self, serializer):
        department = serializer.validated_data["department"]
        if not user_has_department_access(self.request.user, department):
            raise PermissionDenied("No access to selected department.")
        serializer.save()


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return EmployeeCreateSerializer
        if self.action in {"update", "partial_update"}:
            return EmployeeUpdateSerializer
        return EmployeeListSerializer

    def get_queryset(self):
        return get_employees_for_user(self.request.user)


class AssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_assignments_for_user(self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return EmployeeAssignmentCreateSerializer
        if self.action in {"update", "partial_update"}:
            return EmployeeAssignmentUpdateSerializer
        return EmployeeAssignmentListSerializer

    def perform_create(self, serializer):
        staff_unit = serializer.validated_data["staff_unit"]
        if not user_has_department_access(self.request.user, staff_unit.department):
            raise PermissionDenied("No access to selected department.")
        serializer.save()

    @action(detail=False, methods=["post"], url_path="transfer")
    def transfer(self, request):
        serializer = TransferEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_staff_unit = serializer.validated_data["new_staff_unit"]
        if not user_has_department_access(request.user, new_staff_unit.department):
            raise PermissionDenied("No access to selected department.")
        assignment = serializer.save()
        return Response(EmployeeAssignmentListSerializer(assignment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="close")
    def close(self, request, pk=None):
        assignment = self.get_queryset().filter(pk=pk).first()
        if not assignment:
            raise PermissionDenied("Assignment not found or no access.")
        serializer = CloseAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        closed_assignment = close_assignment(
            assignment=assignment,
            end_date=serializer.validated_data["end_date"],
            note=serializer.validated_data.get("note", ""),
        )
        return Response(EmployeeAssignmentListSerializer(closed_assignment).data)
