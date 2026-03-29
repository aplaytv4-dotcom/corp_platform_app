from django.contrib import admin

from staff.models import Employee, EmployeeAssignment, Position, StaffUnit


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "short_name")


@admin.register(StaffUnit)
class StaffUnitAdmin(admin.ModelAdmin):
    list_display = ("unit_number", "department", "staff_position", "is_active")
    list_filter = ("department", "is_active")
    search_fields = ("unit_number", "department__name", "staff_position__name")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("short_fio", "personnel_number", "is_active")
    list_filter = ("is_active",)
    search_fields = ("last_name", "first_name", "middle_name", "personnel_number", "short_fio")


@admin.register(EmployeeAssignment)
class EmployeeAssignmentAdmin(admin.ModelAdmin):
    list_display = ("employee", "staff_unit", "actual_position", "start_date", "end_date", "is_current")
    list_filter = ("is_current", "staff_unit__department")
    search_fields = ("employee__short_fio", "employee__personnel_number", "staff_unit__unit_number")
