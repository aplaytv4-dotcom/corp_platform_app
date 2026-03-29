from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from common.models import TimeStampedModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.MANAGER)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("role", User.Role.ADMIN)
        extra_fields.setdefault("scope_type", User.ScopeType.ALL)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(username, password, **extra_fields)


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"

    class ScopeType(models.TextChoices):
        ALL = "all", "All"
        MANAGEMENT = "management", "Management"
        DEPARTMENT = "department", "Department"

    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices)
    scope_type = models.CharField(max_length=20, choices=ScopeType.choices, default=ScopeType.ALL)
    management = models.ForeignKey(
        "organization.Management",
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        "organization.Department",
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        ordering = ["username"]

    def clean(self):
        errors = {}
        if self.role == self.Role.ADMIN:
            if self.scope_type != self.ScopeType.ALL:
                errors["scope_type"] = "Admin must have all scope."
        if self.scope_type == self.ScopeType.MANAGEMENT and not self.management_id:
            errors["management"] = "Management is required for management scope."
        if self.scope_type == self.ScopeType.DEPARTMENT and not self.department_id:
            errors["department"] = "Department is required for department scope."
        if self.scope_type == self.ScopeType.ALL:
            self.management = None
            self.department = None
        if self.scope_type == self.ScopeType.MANAGEMENT:
            self.department = None
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.username
