from django.db import transaction

from organization.models import Department, Management


@transaction.atomic
def create_management(validated_data):
    return Management.objects.create(**validated_data)


@transaction.atomic
def update_management(instance, validated_data):
    for field, value in validated_data.items():
        setattr(instance, field, value)
    instance.full_clean()
    instance.save()
    return instance


@transaction.atomic
def create_department(validated_data):
    return Department.objects.create(**validated_data)


@transaction.atomic
def update_department(instance, validated_data):
    for field, value in validated_data.items():
        setattr(instance, field, value)
    instance.full_clean()
    instance.save()
    return instance
