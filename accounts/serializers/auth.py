from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    device_id= serializers.CharField()

