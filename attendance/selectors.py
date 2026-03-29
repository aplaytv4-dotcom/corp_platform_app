from django.db.models import Count, Q

from attendance.models import AbsenceReason, AttendanceSheet
from common.permissions import user_has_department_access
from organization.selectors import get_departments_for_user
from staff.selectors import get_assignments_for_department_on_date


def get_absence_reasons_queryset():
    return AbsenceReason.objects.filter(is_active=True).select_related("created_by")


def get_attendance_sheets_for_user(user):
    departments = get_departments_for_user(user)
    return AttendanceSheet.objects.select_related("department", "department__management", "created_by", "updated_by").filter(
        department__in=departments
    )


def get_sheet_or_none_for_user(user, sheet_id):
    return get_attendance_sheets_for_user(user).filter(id=sheet_id).first()


def build_daily_report_data(sheet):
    valid_assignments = list(get_assignments_for_department_on_date(sheet.department, sheet.date))
    valid_by_employee_id = {assignment.employee_id: assignment for assignment in valid_assignments}
    items = [
        item
        for item in sheet.items.select_related("employee", "absence_reason").all()
        if item.employee_id in valid_by_employee_id
    ]
    return {
        "sheet_id": sheet.id,
        "date": sheet.date.isoformat(),
        "department": sheet.department.name,
        "rows": [
            {
                "employee_id": item.employee_id,
                "employee": item.employee.short_fio,
                "actual_position": valid_by_employee_id[item.employee_id].actual_position.name,
                "personnel_number": item.employee.personnel_number,
                "status": item.status,
                "absence_reason": item.absence_reason.name if item.absence_reason else "",
                "note": item.note,
            }
            for item in items
        ],
    }


def build_summary_report_data(user, start_date, end_date):
    departments = get_departments_for_user(user)
    sheets = AttendanceSheet.objects.filter(
        department__in=departments,
        date__gte=start_date,
        date__lte=end_date,
    )
    rows = (
        sheets.values("department__name")
        .annotate(
            present_count=Count("items", filter=Q(items__status="present")),
            absent_count=Count("items", filter=Q(items__status="absent")),
        )
        .order_by("department__name")
    )
    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "rows": list(rows),
    }


def can_access_sheet(user, sheet):
    return user_has_department_access(user, sheet.department)
