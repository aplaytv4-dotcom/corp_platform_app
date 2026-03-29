from django.db.models import Q

from organization.selectors import get_departments_for_user
from staff.models import Employee, EmployeeAssignment, Position, StaffUnit


def get_positions_for_user(user):
    return Position.objects.filter(is_active=True)


def get_staff_units_for_user(user):
    departments = get_departments_for_user(user)
    return StaffUnit.objects.select_related("department", "staff_position", "department__management").filter(
        department__in=departments
    )


def get_employees_for_user(user):
    if user.role == "admin" or user.scope_type == "all":
        return Employee.objects.filter(is_active=True)
    departments = get_departments_for_user(user)
    return Employee.objects.filter(
        is_active=True,
        assignments__staff_unit__department__in=departments,
    ).distinct()


def get_assignments_for_user(user):
    departments = get_departments_for_user(user)
    return EmployeeAssignment.objects.select_related(
        "employee",
        "staff_unit",
        "staff_unit__department",
        "staff_unit__department__management",
        "staff_unit__staff_position",
        "actual_position",
    ).filter(staff_unit__department__in=departments)


def get_assignments_for_department_on_date(department, target_date):
    return EmployeeAssignment.objects.select_related(
        "employee",
        "staff_unit",
        "staff_unit__staff_position",
        "actual_position",
        "staff_unit__department",
    ).filter(
        is_current=True,
        staff_unit__department=department,
        staff_unit__is_active=True,
        employee__is_active=True,
        start_date__lte=target_date,
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=target_date)
    )
