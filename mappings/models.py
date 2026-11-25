"""
mappings/models.py  —  PatientDoctorMapping model.
"""
from django.conf import settings
from django.db import models

from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="doctor_mappings",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="patient_mappings",
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assignments",
    )
    notes = models.TextField(blank=True, default="")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "patient_doctor_mappings"
        unique_together = [("patient", "doctor")]
        ordering = ["-assigned_at"]
        verbose_name = "Patient-Doctor Mapping"
        verbose_name_plural = "Patient-Doctor Mappings"

    def __str__(self) -> str:
        return f"{self.patient} → {self.doctor}"
