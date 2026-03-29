from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


User = get_user_model()


@transaction.atomic
def create_user(validated_data):
    password = validated_data.pop("password")
    user = User(**validated_data)
    validate_password(password, user)
    user.set_password(password)
    user.full_clean()
    user.save()
    return user


@transaction.atomic
def update_user(instance, validated_data):
    password = validated_data.pop("password", None)
    for field, value in validated_data.items():
        setattr(instance, field, value)
    if password:
        validate_password(password, instance)
        instance.set_password(password)
    instance.full_clean()
    instance.save()
    return instance


@transaction.atomic
def change_password(user, current_password: str, new_password: str):
    if not user.check_password(current_password):
        raise ValidationError({"current_password": "Current password is incorrect."})
    validate_password(new_password, user)
    user.set_password(new_password)
    user.save(update_fields=["password"])
    return user


def ensure_can_manage_users(user):
    if user.role != "admin":
        raise PermissionDenied("Only admin can manage users.")
