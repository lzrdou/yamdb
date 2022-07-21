from rest_framework import serializers

from .models import User


class UserEmailSerializer(serializers.Serializer):
    emali = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = (
            "username",
            "role",
            "email",
            "first_name",
            "last_name",
            "bio",
        )
