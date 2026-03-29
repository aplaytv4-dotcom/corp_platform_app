from django.contrib import admin

from organization.models import Department, Management


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "management", "is_active")
    list_filter = ("management", "is_active")
    search_fields = ("name", "code", "management__name")
