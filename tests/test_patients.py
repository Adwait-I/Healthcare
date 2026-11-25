"""
tests/test_patients.py  —  Patient CRUD + ownership tests.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .helpers import create_user, auth_client, PATIENT_PAYLOAD


class PatientCRUDTests(APITestCase):
    list_url = reverse("patient-list-create")

    def setUp(self):
        self.user = create_user()
        self.client = auth_client(self.user)
        self.other_user = create_user(email="other@test.com")
        self.other_client = auth_client(self.other_user)

    # ── Create ────────────────────────────────────────────────────────────────

    def test_create_patient_success(self):
        resp = self.client.post(self.list_url, PATIENT_PAYLOAD, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["full_name"], PATIENT_PAYLOAD["full_name"])

    def test_create_patient_missing_required_field(self):
        payload = {**PATIENT_PAYLOAD}
        del payload["full_name"]
        resp = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_patient_invalid_gender(self):
        resp = self.client.post(self.list_url, {**PATIENT_PAYLOAD, "gender": "X"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_patient_invalid_phone(self):
        resp = self.client.post(self.list_url, {**PATIENT_PAYLOAD, "phone_number": "123"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_patient_requires_auth(self):
        from rest_framework.test import APIClient
        resp = APIClient().post(self.list_url, PATIENT_PAYLOAD, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── List ──────────────────────────────────────────────────────────────────

    def test_list_patients_own_only(self):
        """User only sees their own patients."""
        self.client.post(self.list_url, PATIENT_PAYLOAD, format="json")
        self.other_client.post(
            self.list_url,
            {**PATIENT_PAYLOAD, "phone_number": "1234567890"},
            format="json",
        )
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_list_patients_empty(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, [])

    # ── Detail ────────────────────────────────────────────────────────────────

    def _create_patient(self):
        resp = self.client.post(self.list_url, PATIENT_PAYLOAD, format="json")
        return resp.data["id"]

    def test_retrieve_own_patient(self):
        pid = self._create_patient()
        resp = self.client.get(reverse("patient-detail", args=[pid]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["id"], pid)

    def test_retrieve_other_user_patient_returns_404(self):
        pid = self._create_patient()
        resp = self.other_client.get(reverse("patient-detail", args=[pid]))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # ── Update ────────────────────────────────────────────────────────────────

    def test_full_update_patient(self):
        pid = self._create_patient()
        resp = self.client.put(
            reverse("patient-detail", args=[pid]),
            {**PATIENT_PAYLOAD, "full_name": "Updated Name"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["full_name"], "Updated Name")

    def test_partial_update_patient(self):
        pid = self._create_patient()
        resp = self.client.patch(
            reverse("patient-detail", args=[pid]),
            {"full_name": "Partial Update"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["full_name"], "Partial Update")

    def test_update_other_user_patient_returns_404(self):
        pid = self._create_patient()
        resp = self.other_client.put(
            reverse("patient-detail", args=[pid]),
            PATIENT_PAYLOAD,
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # ── Delete ────────────────────────────────────────────────────────────────

    def test_delete_own_patient(self):
        pid = self._create_patient()
        resp = self.client.delete(reverse("patient-detail", args=[pid]))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get(reverse("patient-detail", args=[pid]))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_other_user_patient_returns_404(self):
        pid = self._create_patient()
        resp = self.other_client.delete(reverse("patient-detail", args=[pid]))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
