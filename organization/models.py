from django.db import models

from common.models import TimeStampedModel


class Management(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Управление"
        verbose_name_plural = "Управления"

    def __str__(self):
        return self.name


class Department(TimeStampedModel):
    management = models.ForeignKey(Management, on_delete=models.PROTECT, related_name="departments")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["management__name", "name"]
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"
        constraints = [
            models.UniqueConstraint(fields=["management", "code"], name="uniq_department_code_per_management"),
        ]

    def __str__(self):
        return f"{self.management.code} - {self.name}"
