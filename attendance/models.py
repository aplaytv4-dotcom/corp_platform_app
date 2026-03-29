from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel


class AbsenceReason(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    is_system = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_absence_reasons")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Причина отсутствия"
        verbose_name_plural = "Причины отсутствия"

    def __str__(self):
        return self.name


class AttendanceSheet(TimeStampedModel):
    date = models.DateField()
    department = models.ForeignKey("organization.Department", on_delete=models.PROTECT, related_name="attendance_sheets")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_attendance_sheets")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="updated_attendance_sheets")

    class Meta:
        ordering = ["-date", "department__name"]
        verbose_name = "Табель"
        verbose_name_plural = "Табели"
        constraints = [
            models.UniqueConstraint(fields=["date", "department"], name="uniq_sheet_per_day_department"),
        ]

    def __str__(self):
        return f"{self.department.name} - {self.date}"


class AttendanceSheetItem(TimeStampedModel):
    class Status(models.TextChoices):
        PRESENT = "present", _("Присутствует")
        ABSENT = "absent", _("Отсутствует")

    attendance_sheet = models.ForeignKey(AttendanceSheet, on_delete=models.CASCADE, related_name="items")
    employee = models.ForeignKey("staff.Employee", on_delete=models.PROTECT, related_name="attendance_items")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT)
    absence_reason = models.ForeignKey(
        AbsenceReason,
        on_delete=models.PROTECT,
        related_name="attendance_items",
        null=True,
        blank=True,
    )
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["employee__last_name", "employee__first_name"]
        verbose_name = "Строка табеля"
        verbose_name_plural = "Строки табеля"
        constraints = [
            models.UniqueConstraint(fields=["attendance_sheet", "employee"], name="uniq_employee_per_sheet"),
        ]

    def clean(self):
        if self.status == self.Status.ABSENT and not self.absence_reason_id:
            raise ValidationError({"absence_reason": _("Для отсутствия нужно указать причину.")})
        if self.status == self.Status.PRESENT:
            self.absence_reason = None

    def __str__(self):
        return f"{self.employee.short_fio} - {self.status}"
