"""
doctors/models.py  —  Doctor model.
"""
from django.conf import settings
from django.db import models


class Doctor(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctors_created",
        help_text="Audit: user who created this doctor record.",
    )
    full_name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, default="")
    years_of_experience = models.PositiveSmallIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "doctors"
        ordering = ["full_name"]
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self) -> str:
        return f"Dr. {self.full_name} ({self.specialization})"
