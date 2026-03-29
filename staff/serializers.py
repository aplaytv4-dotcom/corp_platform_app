from rest_framework import serializers

from staff.models import Employee, EmployeeAssignment, Position, StaffUnit
from staff.services import create_assignment, transfer_employee, update_assignment


class PositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["id", "name", "short_name", "is_active"]


class PositionCreateSerializer(PositionListSerializer):
    pass


class PositionUpdateSerializer(PositionListSerializer):
    pass


class StaffUnitListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    management_name = serializers.CharField(source="department.management.name", read_only=True)
    staff_position_name = serializers.CharField(source="staff_position.name", read_only=True)
    current_employee = serializers.SerializerMethodField()
    occupancy_status = serializers.SerializerMethodField()

    class Meta:
        model = StaffUnit
        fields = [
            "id",
            "department",
            "department_name",
            "management_name",
            "staff_position",
            "staff_position_name",
            "unit_number",
            "occupancy_status",
            "current_employee",
            "is_active",
        ]

    def get_current_employee(self, obj):
        current_assignment = obj.assignments.filter(is_current=True).select_related("employee").first()
        if not current_assignment:
            return ""
        return current_assignment.employee.short_fio

    def get_occupancy_status(self, obj):
        return "occupied" if obj.assignments.filter(is_current=True).exists() else "vacant"


class StaffUnitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUnit
        fields = ["id", "department", "staff_position", "unit_number", "is_active"]


class StaffUnitUpdateSerializer(StaffUnitCreateSerializer):
    pass


class EmployeeListSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    staff_position_name = serializers.SerializerMethodField()
    actual_position_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "short_fio",
            "personnel_number",
            "department_name",
            "staff_position_name",
            "actual_position_name",
            "is_active",
        ]

    def _get_current_assignment(self, obj):
        if hasattr(obj, "_current_assignment_cache"):
            return obj._current_assignment_cache
        assignment = obj.assignments.filter(is_current=True).select_related(
            "staff_unit__department",
            "staff_unit__staff_position",
            "actual_position",
        ).first()
        obj._current_assignment_cache = assignment
        return assignment

    def get_department_name(self, obj):
        assignment = self._get_current_assignment(obj)
        return assignment.staff_unit.department.name if assignment else ""

    def get_staff_position_name(self, obj):
        assignment = self._get_current_assignment(obj)
        return assignment.staff_unit.staff_position.name if assignment else ""

    def get_actual_position_name(self, obj):
        assignment = self._get_current_assignment(obj)
        return assignment.actual_position.name if assignment else ""


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "personnel_number",
            "is_active",
        ]


class EmployeeUpdateSerializer(EmployeeCreateSerializer):
    pass


class EmployeeAssignmentListSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.short_fio", read_only=True)
    department_name = serializers.CharField(source="staff_unit.department.name", read_only=True)
    staff_unit_number = serializers.CharField(source="staff_unit.unit_number", read_only=True)
    actual_position_name = serializers.CharField(source="actual_position.name", read_only=True)

    class Meta:
        model = EmployeeAssignment
        fields = [
            "id",
            "employee",
            "employee_name",
            "staff_unit",
            "staff_unit_number",
            "department_name",
            "actual_position",
            "actual_position_name",
            "start_date",
            "end_date",
            "is_current",
            "note",
        ]


class EmployeeAssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAssignment
        fields = [
            "id",
            "employee",
            "staff_unit",
            "actual_position",
            "start_date",
            "end_date",
            "is_current",
            "note",
        ]

    def create(self, validated_data):
        return create_assignment(validated_data)


class EmployeeAssignmentUpdateSerializer(EmployeeAssignmentCreateSerializer):
    def update(self, instance, validated_data):
        return update_assignment(instance, validated_data)


class TransferEmployeeSerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.filter(is_active=True))
    new_staff_unit = serializers.PrimaryKeyRelatedField(queryset=StaffUnit.objects.filter(is_active=True))
    actual_position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.filter(is_active=True))
    start_date = serializers.DateField()
    note = serializers.CharField(required=False, allow_blank=True)

    def save(self, **kwargs):
        return transfer_employee(**self.validated_data)


class CloseAssignmentSerializer(serializers.Serializer):
    end_date = serializers.DateField()
    note = serializers.CharField(required=False, allow_blank=True)
