from django.urls import reverse
from rest_framework import status
from upshot.common.tests.test_mixins import UserAPITestCase
from upshot.common.utils.otp_helpers import generate_otp_for_receiver
from upshot.common.utils.otl_helpers import generate_otl_for_receiver


class PasswordAPITestCase(UserAPITestCase):
    def setUp(self):
        super().setUp()
        self.login_data = self.login()

    def login(self):
        url = reverse("api-authentication:jwt-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        return {**response.json(), "status_code": response.status_code}

    def authenticate_client(self):
        token = self.login_data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def check_password_changed_unauthorized_401(self):
        self.login_data = self.login()
        status_code = self.login_data.get("status_code")
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_passwords_not_strong_400_fail(self):
        self.authenticate_client()

        url = reverse("api-authentication:change-password")
        data = {
            "password": self.user_data.get("weak_password"),
            "repeat_password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_passwords_not_match_400_fail(self):
        self.authenticate_client()

        url = reverse("api-authentication:change-password")
        data = {
            "password": self.user_data.get("strong_password"),
            "repeat_password": self.user_data.get("strong_password") + "test",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_200_ok(self):
        self.authenticate_client()

        url = reverse("api-authentication:change-password")
        data = {
            "password": self.user_data.get("strong_password"),
            "repeat_password": self.user_data.get("strong_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.subTest("check if password changed"):
            self.check_password_changed_unauthorized_401()

    def test_reset_password_change_otp_200_ok(self):
        url = reverse("api-authentication:reset-password-phone-otp")
        receiver = self.user.profile.get_primary_phone_number()
        otp = generate_otp_for_receiver(receiver)
        data = {
            "receiver": receiver,
            "otp": otp,
            "password": self.user_data.get("strong_password"),
            "repeat_password": self.user_data.get("strong_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_reset_email_otl_20_ok(self):
        email = self.user.profile.get_primary_email()
        otl = generate_otl_for_receiver(email)
        data = {
            "email": email,
            "otl": otl,
            "password": self.user_data.get("strong_password"),
            "repeat_password": self.user_data.get("strong_password"),
        }

        url = reverse("api-authentication:reset-password-email-otl", args=[otl])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_reset_email_otl_400_fail(self):
        email = self.user.profile.get_primary_email()
        otl = generate_otl_for_receiver(email)
        data = {
            "email": email,
            "otl": "wrong_otl",
            "password": self.user_data.get("strong_password"),
            "repeat_password": self.user_data.get("strong_password"),
        }

        url = reverse("api-authentication:reset-password-email-otl", args=[otl])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
