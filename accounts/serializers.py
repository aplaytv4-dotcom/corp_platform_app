from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.services import change_password, create_user, update_user


User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    management_name = serializers.CharField(source="management.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "role",
            "scope_type",
            "management",
            "management_name",
            "department",
            "department_name",
            "is_active",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "full_name",
            "role",
            "scope_type",
            "management",
            "department",
            "is_active",
        ]

    def create(self, validated_data):
        return create_user(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "full_name",
            "role",
            "scope_type",
            "management",
            "department",
            "is_active",
        ]

    def update(self, instance, validated_data):
        return update_user(instance, validated_data)


class MeSerializer(UserListSerializer):
    class Meta(UserListSerializer.Meta):
        fields = UserListSerializer.Meta.fields


class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["role"] = user.role
        token["scope_type"] = user.scope_type
        return token

    def validate(self, attrs):
        authenticate_kwargs = {
            "username": attrs.get("username"),
            "password": attrs.get("password"),
        }
        user = authenticate(**authenticate_kwargs)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        data = super().validate(attrs)
        data["user"] = MeSerializer(self.user).data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def save(self, **kwargs):
        return change_password(self.context["request"].user, self.validated_data["current_password"], self.validated_data["new_password"])
