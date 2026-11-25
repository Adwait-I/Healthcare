"""
accounts/serializers.py  —  Serializers for user registration and profile.
"""
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_\-])[A-Za-z\d@$!%*#?&_\-]{8,}$"
)


class UserRegisterSerializer(serializers.ModelSerializer):
    """Validates and creates a new user account."""

    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("id", "name", "email", "password", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_password(self, value: str) -> str:
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters and contain uppercase, "
                "lowercase, digit, and special character (@$!%*#?&_-)."
            )
        return value

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Read-only profile view of the authenticated user."""

    class Meta:
        model = User
        fields = ("id", "name", "email", "created_at", "updated_at")
        read_only_fields = fields
