from rest_framework.permissions import BasePermission


def user_has_department_access(user, department) -> bool:
    if not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "role", None) == "admin":
        return True
    if getattr(user, "scope_type", None) == "all":
        return True
    if getattr(user, "scope_type", None) == "management":
        return bool(user.management_id and department.management_id == user.management_id)
    if getattr(user, "scope_type", None) == "department":
        return bool(user.department_id and department.id == user.department_id)
    return False


def user_has_management_access(user, management) -> bool:
    if not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "role", None) == "admin":
        return True
    if getattr(user, "scope_type", None) == "all":
        return True
    if getattr(user, "scope_type", None) == "management":
        return bool(user.management_id and management.id == user.management_id)
    if getattr(user, "scope_type", None) == "department":
        return bool(user.department_id and user.department.management_id == management.id)
    return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "admin")


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "manager")


class HasDepartmentAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        department = getattr(obj, "department", None)
        if department is None and hasattr(obj, "staff_unit"):
            department = obj.staff_unit.department
        if department is None and hasattr(obj, "attendance_sheet"):
            department = obj.attendance_sheet.department
        if department is None and hasattr(obj, "management"):
            return user_has_management_access(request.user, obj.management)
        if department is None:
            return request.user.role == "admin"
        return user_has_department_access(request.user, department)
