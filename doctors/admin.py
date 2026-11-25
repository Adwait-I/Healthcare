"""doctors/admin.py"""
from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "specialization", "license_number", "years_of_experience", "created_at"]
    list_filter = ["specialization", "created_at"]
    search_fields = ["full_name", "license_number", "email"]
    readonly_fields = ["created_at", "updated_at"]
