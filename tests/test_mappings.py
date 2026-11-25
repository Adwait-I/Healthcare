"""
tests/test_mappings.py  —  Patient-Doctor mapping tests.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from patients.models import Patient
from doctors.models import Doctor
from .helpers import create_user, auth_client, PATIENT_PAYLOAD, DOCTOR_PAYLOAD


class MappingTests(APITestCase):
    mapping_list_url = reverse("mapping-list-create")

    def setUp(self):
        self.user = create_user()
        self.client = auth_client(self.user)

        # Create a patient and doctor directly via ORM for speed
        self.patient = Patient.objects.create(created_by=self.user, **PATIENT_PAYLOAD)
        self.doctor = Doctor.objects.create(created_by=self.user, **DOCTOR_PAYLOAD)

    # ── Create Mapping ────────────────────────────────────────────────────────

    def test_create_mapping_success(self):
        resp = self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["patient"], self.patient.pk)
        self.assertEqual(resp.data["doctor"], self.doctor.pk)
        self.assertEqual(resp.data["patient_name"], self.patient.full_name)
        self.assertEqual(resp.data["doctor_name"], self.doctor.full_name)

    def test_create_mapping_duplicate_raises_400(self):
        self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        resp = self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_mapping_invalid_patient_id(self):
        resp = self.client.post(
            self.mapping_list_url,
            {"patient": 9999, "doctor": self.doctor.pk},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_mapping_invalid_doctor_id(self):
        resp = self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": 9999},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_mapping_requires_auth(self):
        from rest_framework.test import APIClient
        resp = APIClient().post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── List Mappings ─────────────────────────────────────────────────────────

    def test_list_all_mappings(self):
        self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        resp = self.client.get(self.mapping_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    # ── Mappings by Patient ───────────────────────────────────────────────────

    def test_get_mappings_by_patient(self):
        self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        url = reverse("mapping-by-patient", args=[self.patient.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["patient_id"], self.patient.pk)
        self.assertEqual(len(resp.data["mappings"]), 1)

    def test_get_mappings_nonexistent_patient_returns_404(self):
        url = reverse("mapping-by-patient", args=[9999])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_mappings_patient_no_doctors(self):
        url = reverse("mapping-by-patient", args=[self.patient.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["mappings"], [])

    # ── Delete Mapping ────────────────────────────────────────────────────────

    def test_delete_mapping_success(self):
        mapping_resp = self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        mapping_id = mapping_resp.data["id"]
        del_resp = self.client.delete(reverse("mapping-delete", args=[mapping_id]))
        self.assertEqual(del_resp.status_code, status.HTTP_200_OK)
        self.assertIn("detail", del_resp.data)

    def test_delete_nonexistent_mapping_returns_404(self):
        resp = self.client.delete(reverse("mapping-delete", args=[9999]))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_mapping_requires_auth(self):
        from rest_framework.test import APIClient
        mapping_resp = self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        mapping_id = mapping_resp.data["id"]
        resp = APIClient().delete(reverse("mapping-delete", args=[mapping_id]))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── After delete, re-mapping allowed ─────────────────────────────────────

    def test_remap_after_delete(self):
        mapping_resp = self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        mapping_id = mapping_resp.data["id"]
        self.client.delete(reverse("mapping-delete", args=[mapping_id]))
        resp = self.client.post(
            self.mapping_list_url,
            {"patient": self.patient.pk, "doctor": self.doctor.pk},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
