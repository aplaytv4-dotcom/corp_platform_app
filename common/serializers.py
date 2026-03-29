from rest_framework import serializers


class HealthcheckSerializer(serializers.Serializer):
    status = serializers.CharField()
