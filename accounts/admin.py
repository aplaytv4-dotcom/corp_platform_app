from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "username",
        "full_name",
        "role",
        "scope_type",
        "management",
        "department",
        "is_active",
        "is_staff",
    )
    list_filter = ("role", "scope_type", "is_active", "is_staff")
    search_fields = ("username", "full_name")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        (
            "Access",
            {
                "fields": (
                    "role",
                    "scope_type",
                    "management",
                    "department",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "full_name",
                    "role",
                    "scope_type",
                    "management",
                    "department",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
