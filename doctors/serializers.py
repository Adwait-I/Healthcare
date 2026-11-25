"""
doctors/serializers.py  —  Doctor serializers.
"""
from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for Doctor."""

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Doctor
        fields = (
            "id",
            "created_by",
            "full_name",
            "specialization",
            "license_number",
            "phone_number",
            "email",
            "years_of_experience",
            "consultation_fee",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_license_number(self, value: str) -> str:
        value = value.strip().upper()
        qs = Doctor.objects.filter(license_number=value)
        # Exclude current instance on updates
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A doctor with this license number already exists.")
        return value

    def validate_consultation_fee(self, value) -> float:
        if value < 0:
            raise serializers.ValidationError("Consultation fee cannot be negative.")
        return value


class DoctorReadSerializer(DoctorSerializer):
    """Read serializer that exposes created_by as an ID."""

    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
