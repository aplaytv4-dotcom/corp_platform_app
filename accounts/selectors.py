from django.contrib.auth import get_user_model


User = get_user_model()


def get_users_queryset():
    return User.objects.select_related("management", "department").all()
