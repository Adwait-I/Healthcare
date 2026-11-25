"""
patients/serializers.py  —  Patient serializers.
"""
from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for Patient."""

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Patient
        fields = (
            "id",
            "created_by",
            "full_name",
            "date_of_birth",
            "gender",
            "phone_number",
            "address",
            "medical_history",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_phone_number(self, value: str) -> str:
        digits = "".join(c for c in value if c.isdigit())
        if not (7 <= len(digits) <= 15):
            raise serializers.ValidationError("Phone number must have 7–15 digits.")
        return value


class PatientReadSerializer(PatientSerializer):
    """Read serializer that exposes created_by as an ID."""

    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
