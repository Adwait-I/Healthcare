"""
tests/helpers.py  —  Shared test helpers.
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_user(email="user@test.com", name="Test User", password="SecurePass1@"):
    return User.objects.create_user(email=email, name=name, password=password)


def auth_client(user) -> APIClient:
    """Return an APIClient with Bearer token set for *user*."""
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


PATIENT_PAYLOAD = {
    "full_name": "Jane Doe",
    "date_of_birth": "1990-01-15",
    "gender": "F",
    "phone_number": "9876543210",
    "address": "123 Main St",
    "medical_history": "No known allergies.",
}

DOCTOR_PAYLOAD = {
    "full_name": "Dr. John Smith",
    "specialization": "Cardiology",
    "license_number": "LIC-001",
    "phone_number": "9123456789",
    "email": "drsmith@hospital.com",
    "years_of_experience": 10,
    "consultation_fee": "500.00",
}
