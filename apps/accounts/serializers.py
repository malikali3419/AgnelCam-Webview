from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    personal_access_token = serializers.CharField(
        max_length=255, required=True, help_text="Personal Access Token is required."
    )
