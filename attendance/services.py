from django.db import transaction
from rest_framework.exceptions import ValidationError

from attendance.models import AttendanceSheet, AttendanceSheetItem
from staff.selectors import get_assignments_for_department_on_date


@transaction.atomic
def open_or_create_attendance_sheet(*, date, department, user):
    sheet, created = AttendanceSheet.objects.select_for_update().get_or_create(
        date=date,
        department=department,
        defaults={
            "created_by": user,
            "updated_by": user,
        },
    )
    assignments = get_assignments_for_department_on_date(department, date)
    existing_employee_ids = set(sheet.items.values_list("employee_id", flat=True))
    new_items = []
    for assignment in assignments:
        if assignment.employee_id in existing_employee_ids:
            continue
        new_items.append(
            AttendanceSheetItem(
                attendance_sheet=sheet,
                employee=assignment.employee,
                status=AttendanceSheetItem.Status.PRESENT,
            )
        )
    if new_items:
        AttendanceSheetItem.objects.bulk_create(new_items)
    if not created:
        sheet.updated_by = user
        sheet.save(update_fields=["updated_by", "updated_at"])
    return sheet


@transaction.atomic
def bulk_update_attendance_items(*, sheet_id, items, user):
    sheet = AttendanceSheet.objects.select_for_update().select_related("department").filter(id=sheet_id).first()
    if not sheet:
        raise ValidationError({"sheet_id": "Attendance sheet not found."})

    employee_ids = [item["employee_id"] for item in items]
    sheet_items = {
        item.employee_id: item
        for item in AttendanceSheetItem.objects.select_for_update().filter(
            attendance_sheet_id=sheet_id,
            employee_id__in=employee_ids,
        )
    }

    for payload in items:
        item = sheet_items.get(payload["employee_id"])
        if item is None:
            raise ValidationError({"employee_id": f"Employee {payload['employee_id']} is not part of the sheet."})
        status = payload["status"]
        absence_reason = payload.get("absence_reason")
        if status == AttendanceSheetItem.Status.ABSENT and not absence_reason:
            raise ValidationError({"absence_reason": "Absence reason is required for absent status."})
        item.status = status
        item.absence_reason = absence_reason if status == AttendanceSheetItem.Status.ABSENT else None
        item.note = payload.get("note", "")
        item.full_clean()
        item.save()

    sheet.updated_by = user
    sheet.save(update_fields=["updated_by", "updated_at"])
    return sheet
