"""patients/admin.py"""
from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["full_name", "gender", "phone_number", "created_by", "created_at"]
    list_filter = ["gender", "created_at"]
    search_fields = ["full_name", "phone_number"]
    readonly_fields = ["created_at", "updated_at"]
