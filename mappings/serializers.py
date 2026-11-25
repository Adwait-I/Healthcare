"""
mappings/serializers.py  —  PatientDoctorMapping serializers.
"""
from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class MappingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a patient-doctor mapping."""

    assigned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "doctor", "assigned_by", "notes", "assigned_at")
        read_only_fields = ("id", "assigned_at")

    def validate(self, attrs: dict) -> dict:
        patient: Patient = attrs["patient"]
        doctor: Doctor = attrs["doctor"]

        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError(
                {"non_field_errors": f"Doctor '{doctor.full_name}' is already assigned to patient '{patient.full_name}'."}
            )
        return attrs


class MappingReadSerializer(serializers.ModelSerializer):
    """Serializer for reading mappings with nested info."""

    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.full_name", read_only=True)
    doctor_specialization = serializers.CharField(source="doctor.specialization", read_only=True)
    assigned_by_email = serializers.CharField(source="assigned_by.email", read_only=True, default=None)

    class Meta:
        model = PatientDoctorMapping
        fields = (
            "id",
            "patient",
            "patient_name",
            "doctor",
            "doctor_name",
            "doctor_specialization",
            "assigned_by",
            "assigned_by_email",
            "notes",
            "assigned_at",
        )
