from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from attendance.models import AbsenceReason, AttendanceSheet, AttendanceSheetItem
from organization.models import Department, Management
from staff.models import Employee, EmployeeAssignment, Position, StaffUnit


class AttendanceReportTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username="admin",
            password="secret123",
            full_name="System Admin",
        )
        self.client.force_authenticate(self.user)

        self.management = Management.objects.create(name="Main Office", code="MO")
        self.department = Department.objects.create(
            management=self.management,
            name="HR Department",
            code="HR",
        )
        self.position = Position.objects.create(
            name="Department Head",
            short_name="Head",
            hierarchy_order=100,
        )
        self.staff_unit = StaffUnit.objects.create(
            department=self.department,
            staff_position=self.position,
            unit_number="001",
        )
        self.employee = Employee.objects.create(
            last_name="Ivanov",
            first_name="Ivan",
            middle_name="Ivanovich",
            personnel_number="0001",
        )
        EmployeeAssignment.objects.create(
            employee=self.employee,
            staff_unit=self.staff_unit,
            actual_position=self.position,
            start_date=date(2026, 4, 1),
            is_current=True,
        )

        self.absence_reason = AbsenceReason.objects.create(
            name="Vacation",
            code="VAC",
            created_by=self.user,
        )

    def _create_sheet_with_item(self, sheet_date, *, status, note=""):
        sheet = AttendanceSheet.objects.create(
            date=sheet_date,
            department=self.department,
            created_by=self.user,
            updated_by=self.user,
        )
        AttendanceSheetItem.objects.create(
            attendance_sheet=sheet,
            employee=self.employee,
            status=status,
            absence_reason=self.absence_reason if status == AttendanceSheetItem.Status.ABSENT else None,
            note=note,
        )
        return sheet

    def test_daily_html_report_is_available(self):
        sheet = self._create_sheet_with_item(
            date(2026, 4, 10),
            status=AttendanceSheetItem.Status.ABSENT,
            note="Annual leave",
        )

        response = self.client.get("/api/reports/daily-attendance-html/", {"sheet_id": sheet.id, "lang": "ru"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")
        content = response.content.decode("utf-8")
        self.assertIn("Ежедневный отчет", content)
        self.assertIn("HR Department", content)
        self.assertIn("Vacation", content)

    def test_summary_html_report_for_period_is_available(self):
        self._create_sheet_with_item(date(2026, 4, 10), status=AttendanceSheetItem.Status.PRESENT)
        self._create_sheet_with_item(date(2026, 4, 11), status=AttendanceSheetItem.Status.ABSENT, note="Vacation")

        response = self.client.get(
            "/api/reports/summary-html/",
            {
                "start_date": "2026-04-10",
                "end_date": "2026-04-11",
                "lang": "ru",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")
        content = response.content.decode("utf-8")
        self.assertIn("Сводный отчет", content)
        self.assertIn("HR Department", content)
        self.assertIn("<td>1</td><td>1</td>", content)

    def test_summary_pdf_report_is_available(self):
        self._create_sheet_with_item(date(2026, 4, 10), status=AttendanceSheetItem.Status.PRESENT)

        response = self.client.get(
            "/api/reports/summary-pdf/",
            {
                "start_date": "2026-04-10",
                "end_date": "2026-04-10",
                "lang": "ru",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))
