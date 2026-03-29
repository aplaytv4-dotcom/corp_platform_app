from rest_framework import serializers

from organization.models import Department, Management
from organization.services import create_department, create_management, update_department, update_management


class ManagementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = ["id", "name", "code", "is_active"]


class ManagementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = ["id", "name", "code", "is_active"]

    def create(self, validated_data):
        return create_management(validated_data)


class ManagementUpdateSerializer(ManagementCreateSerializer):
    def update(self, instance, validated_data):
        return update_management(instance, validated_data)


class DepartmentListSerializer(serializers.ModelSerializer):
    management_name = serializers.CharField(source="management.name", read_only=True)

    class Meta:
        model = Department
        fields = ["id", "management", "management_name", "name", "code", "is_active"]


class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "management", "name", "code", "is_active"]

    def create(self, validated_data):
        return create_department(validated_data)


class DepartmentUpdateSerializer(DepartmentCreateSerializer):
    def update(self, instance, validated_data):
        return update_department(instance, validated_data)
