from django.contrib import admin

from attendance.models import AbsenceReason, AttendanceSheet, AttendanceSheetItem


class AttendanceSheetItemInline(admin.TabularInline):
    model = AttendanceSheetItem
    extra = 0


@admin.register(AbsenceReason)
class AbsenceReasonAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_system", "created_by", "is_active")
    list_filter = ("is_system", "is_active")
    search_fields = ("name", "code")


@admin.register(AttendanceSheet)
class AttendanceSheetAdmin(admin.ModelAdmin):
    list_display = ("date", "department", "created_by", "updated_by")
    list_filter = ("department", "date")
    search_fields = ("department__name",)
    inlines = [AttendanceSheetItemInline]


@admin.register(AttendanceSheetItem)
class AttendanceSheetItemAdmin(admin.ModelAdmin):
    list_display = ("attendance_sheet", "employee", "status", "absence_reason")
    list_filter = ("status", "attendance_sheet__department")
    search_fields = ("employee__short_fio", "employee__personnel_number")
