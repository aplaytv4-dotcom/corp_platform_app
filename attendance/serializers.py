from rest_framework import serializers

from attendance.models import AbsenceReason, AttendanceSheet, AttendanceSheetItem
from attendance.services import bulk_update_attendance_items, open_or_create_attendance_sheet
from organization.models import Department


class AbsenceReasonListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = AbsenceReason
        fields = ["id", "name", "code", "is_system", "created_by", "created_by_name", "is_active"]


class AbsenceReasonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceReason
        fields = ["id", "name", "code", "is_system", "is_active"]

    def create(self, validated_data):
        return AbsenceReason.objects.create(created_by=self.context["request"].user, **validated_data)


class AbsenceReasonUpdateSerializer(AbsenceReasonCreateSerializer):
    pass


class AttendanceSheetItemSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.short_fio", read_only=True)
    personnel_number = serializers.CharField(source="employee.personnel_number", read_only=True)
    absence_reason_name = serializers.CharField(source="absence_reason.name", read_only=True)
    actual_position_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSheetItem
        fields = [
            "id",
            "employee",
            "employee_name",
            "personnel_number",
            "actual_position_name",
            "status",
            "absence_reason",
            "absence_reason_name",
            "note",
        ]

    def get_actual_position_name(self, obj):
        assignment = obj.employee.assignments.filter(is_current=True).select_related("actual_position").first()
        return assignment.actual_position.name if assignment else ""


class AttendanceSheetDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    items = AttendanceSheetItemSerializer(many=True, read_only=True)

    class Meta:
        model = AttendanceSheet
        fields = [
            "id",
            "date",
            "department",
            "department_name",
            "created_by",
            "updated_by",
            "items",
        ]


class OpenAttendanceSheetSerializer(serializers.Serializer):
    date = serializers.DateField()
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.filter(is_active=True))

    def save(self, **kwargs):
        return open_or_create_attendance_sheet(
            date=self.validated_data["date"],
            department=self.validated_data["department"],
            user=self.context["request"].user,
        )


class AttendanceSheetItemBulkRowSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=AttendanceSheetItem.Status.choices)
    absence_reason = serializers.PrimaryKeyRelatedField(
        queryset=AbsenceReason.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )
    note = serializers.CharField(required=False, allow_blank=True)


class BulkUpdateAttendanceSerializer(serializers.Serializer):
    items = AttendanceSheetItemBulkRowSerializer(many=True)

    def save(self, **kwargs):
        return bulk_update_attendance_items(
            sheet_id=self.context["sheet_id"],
            items=self.validated_data["items"],
            user=self.context["request"].user,
        )
