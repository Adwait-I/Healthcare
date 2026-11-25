"""
tests/test_auth.py  —  Authentication endpoint tests.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTests(APITestCase):
    url = reverse("auth-register")

    def _payload(self, **overrides):
        base = {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "password": "SecurePass1@",
        }
        return {**base, **overrides}

    def test_register_success(self):
        resp = self.client.post(self.url, self._payload(), format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", resp.data)
        self.assertIn("access", resp.data["tokens"])
        self.assertIn("refresh", resp.data["tokens"])
        self.assertEqual(resp.data["user"]["email"], "alice@example.com")

    def test_register_duplicate_email(self):
        self.client.post(self.url, self._payload(), format="json")
        resp = self.client.post(self.url, self._payload(), format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_email(self):
        resp = self.client.post(self.url, self._payload(email=""), format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_weak_password(self):
        resp = self.client.post(self.url, self._payload(password="weak"), format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_name(self):
        resp = self.client.post(self.url, self._payload(name=""), format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_email_format(self):
        resp = self.client.post(self.url, self._payload(email="not-an-email"), format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    register_url = reverse("auth-register")
    login_url = reverse("auth-login")

    def setUp(self):
        self.client.post(
            self.register_url,
            {"name": "Bob", "email": "bob@example.com", "password": "SecurePass1@"},
            format="json",
        )

    def test_login_success(self):
        resp = self.client.post(
            self.login_url,
            {"email": "bob@example.com", "password": "SecurePass1@"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data["tokens"])
        self.assertIn("refresh", resp.data["tokens"])

    def test_login_wrong_password(self):
        resp = self.client.post(
            self.login_url,
            {"email": "bob@example.com", "password": "WrongPass1!"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_non_existent_user(self):
        resp = self.client.post(
            self.login_url,
            {"email": "nobody@example.com", "password": "SecurePass1@"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_fields(self):
        resp = self.client.post(self.login_url, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_protected_endpoint_without_token(self):
        resp = self.client.get(reverse("patient-list-create"))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
