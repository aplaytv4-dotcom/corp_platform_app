from common.permissions import user_has_department_access, user_has_management_access
from organization.models import Department, Management


def get_managements_for_user(user):
    queryset = Management.objects.filter(is_active=True)
    if user.role == "admin" or user.scope_type == "all":
        return queryset
    if user.scope_type == "management" and user.management_id:
        return queryset.filter(id=user.management_id)
    if user.scope_type == "department" and user.department_id:
        return queryset.filter(id=user.department.management_id)
    return queryset.none()


def get_departments_for_user(user):
    queryset = Department.objects.select_related("management").filter(is_active=True)
    if user.role == "admin" or user.scope_type == "all":
        return queryset
    if user.scope_type == "management" and user.management_id:
        return queryset.filter(management_id=user.management_id)
    if user.scope_type == "department" and user.department_id:
        return queryset.filter(id=user.department_id)
    return queryset.none()


def can_access_management(user, management):
    return user_has_management_access(user, management)


def can_access_department(user, department):
    return user_has_department_access(user, department)
