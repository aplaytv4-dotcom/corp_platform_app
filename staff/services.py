from django.db import transaction
from rest_framework.exceptions import ValidationError

from staff.models import EmployeeAssignment


@transaction.atomic
def create_assignment(validated_data):
    assignment = EmployeeAssignment(**validated_data)
    assignment.full_clean()
    assignment.save()
    return assignment


@transaction.atomic
def update_assignment(instance, validated_data):
    for field, value in validated_data.items():
        setattr(instance, field, value)
    instance.full_clean()
    instance.save()
    return instance


@transaction.atomic
def transfer_employee(*, employee, new_staff_unit, actual_position, start_date, note=""):
    current_assignment = EmployeeAssignment.objects.select_for_update().filter(
        employee=employee,
        is_current=True,
    ).first()
    if current_assignment and current_assignment.start_date > start_date:
        raise ValidationError({"start_date": "Transfer date cannot be earlier than current assignment start date."})
    if current_assignment:
        current_assignment.is_current = False
        current_assignment.end_date = start_date
        current_assignment.save(update_fields=["is_current", "end_date", "updated_at"])

    new_assignment = EmployeeAssignment(
        employee=employee,
        staff_unit=new_staff_unit,
        actual_position=actual_position,
        start_date=start_date,
        is_current=True,
        note=note,
    )
    new_assignment.full_clean()
    new_assignment.save()
    return new_assignment


@transaction.atomic
def close_assignment(*, assignment, end_date, note=""):
    if not assignment.is_current:
        raise ValidationError({"assignment": "Assignment is already closed."})
    if end_date < assignment.start_date:
        raise ValidationError({"end_date": "End date cannot be earlier than start date."})
    assignment.end_date = end_date
    assignment.is_current = False
    if note:
        assignment.note = note
    assignment.full_clean()
    assignment.save()
    return assignment
