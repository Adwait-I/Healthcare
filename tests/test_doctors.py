"""
tests/test_doctors.py  —  Doctor CRUD tests.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import create_user, auth_client, DOCTOR_PAYLOAD


class DoctorCRUDTests(APITestCase):
    list_url = reverse("doctor-list-create")

    def setUp(self):
        self.user = create_user()
        self.client = auth_client(self.user)

    def _create_doctor(self, payload=None):
        payload = payload or DOCTOR_PAYLOAD
        resp = self.client.post(self.list_url, payload, format="json")
        return resp

    # ── Create ────────────────────────────────────────────────────────────────

    def test_create_doctor_success(self):
        resp = self._create_doctor()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["full_name"], DOCTOR_PAYLOAD["full_name"])
        self.assertEqual(resp.data["license_number"], "LIC-001")  # uppercased

    def test_create_doctor_duplicate_license(self):
        self._create_doctor()
        resp = self._create_doctor({**DOCTOR_PAYLOAD, "full_name": "Another Doctor"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_doctor_negative_fee(self):
        resp = self._create_doctor({**DOCTOR_PAYLOAD, "consultation_fee": "-100"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_doctor_missing_specialization(self):
        payload = {**DOCTOR_PAYLOAD}
        del payload["specialization"]
        resp = self._create_doctor(payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_doctor_requires_auth(self):
        from rest_framework.test import APIClient
        resp = APIClient().post(self.list_url, DOCTOR_PAYLOAD, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── List ──────────────────────────────────────────────────────────────────

    def test_list_doctors(self):
        self._create_doctor()
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    # ── Detail ────────────────────────────────────────────────────────────────

    def test_retrieve_doctor(self):
        did = self._create_doctor().data["id"]
        resp = self.client.get(reverse("doctor-detail", args=[did]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_doctor(self):
        resp = self.client.get(reverse("doctor-detail", args=[9999]))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # ── Update ────────────────────────────────────────────────────────────────

    def test_update_doctor_full(self):
        did = self._create_doctor().data["id"]
        updated = {**DOCTOR_PAYLOAD, "full_name": "Dr. Updated", "license_number": "LIC-001"}
        resp = self.client.put(reverse("doctor-detail", args=[did]), updated, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["full_name"], "Dr. Updated")

    def test_update_doctor_partial(self):
        did = self._create_doctor().data["id"]
        resp = self.client.patch(
            reverse("doctor-detail", args=[did]),
            {"years_of_experience": 15},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["years_of_experience"], 15)

    # ── Delete ────────────────────────────────────────────────────────────────

    def test_delete_doctor(self):
        did = self._create_doctor().data["id"]
        resp = self.client.delete(reverse("doctor-detail", args=[did]))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexistent_doctor(self):
        resp = self.client.delete(reverse("doctor-detail", args=[9999]))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
