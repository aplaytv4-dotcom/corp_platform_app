from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from common.models import TimeStampedModel


class Position(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=100, blank=True)
    hierarchy_order = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-hierarchy_order", "name"]
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.short_name or self.name


class StaffUnit(TimeStampedModel):
    department = models.ForeignKey("organization.Department", on_delete=models.PROTECT, related_name="staff_units")
    staff_position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name="staff_units")
    unit_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["department__name", "unit_number"]
        verbose_name = "Штатная единица"
        verbose_name_plural = "Штатные единицы"
        constraints = [
            models.UniqueConstraint(fields=["department", "unit_number"], name="uniq_staff_unit_number_per_department"),
        ]

    def __str__(self):
        return f"{self.department.code}-{self.unit_number}"


class Employee(TimeStampedModel):
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    short_fio = models.CharField(max_length=255, blank=True)
    personnel_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_name", "first_name", "middle_name"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def save(self, *args, **kwargs):
        initials = f"{self.first_name[:1]}."
        if self.middle_name:
            initials += f"{self.middle_name[:1]}."
        self.short_fio = f"{self.last_name} {initials}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()


class EmployeeAssignment(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="assignments")
    staff_unit = models.ForeignKey(StaffUnit, on_delete=models.PROTECT, related_name="assignments")
    actual_position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name="actual_assignments")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-is_current", "-start_date", "employee__last_name"]
        verbose_name = "Назначение сотрудника"
        verbose_name_plural = "Назначения сотрудников"
        constraints = [
            models.UniqueConstraint(
                fields=["employee"],
                condition=Q(is_current=True),
                name="uniq_current_assignment_per_employee",
            ),
            models.UniqueConstraint(
                fields=["staff_unit"],
                condition=Q(is_current=True),
                name="uniq_current_assignment_per_staff_unit",
            ),
        ]

    def clean(self):
        errors = {}
        if self.end_date and self.end_date < self.start_date:
            errors["end_date"] = _("Дата окончания не может быть раньше даты начала.")
        if self.is_current and self.end_date:
            errors["end_date"] = _("У текущего назначения не может быть даты окончания.")
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.employee} -> {self.staff_unit}"
