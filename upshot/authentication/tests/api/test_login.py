from django.urls import reverse
from rest_framework import status
from upshot.common.tests.test_mixins import UserAPITestCase
from upshot.common.utils.otp_helpers import generate_otp_for_receiver


class JWTAPITestCase(UserAPITestCase):
    def test_jwt_create_auhtorized_200_ok(self):
        url = reverse("api-authentication:jwt-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_unauthorized_401_fail(self):
        url = reverse("api-authentication:jwt-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("strong_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_create_phone_authorized_200_ok(self):
        url = reverse("api-authentication:jwt-create-phone")

        data = {
            "phone_number": self.user_data.get("phone_number"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_phone_wrong_number_unauthorized_400_fail(self):
        url = reverse("api-authentication:jwt-create-phone")
        wrong_phone_number = "09123456789"

        data = {
            "phone_number": wrong_phone_number,
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_create_phone_otp_authorized_200_ok(self):
        url = reverse("api-authentication:jwt-create-phone-otp")
        receiver = self.user_data.get("phone_number")

        requested_otp = generate_otp_for_receiver(receiver)

        data = {
            "receiver": receiver,
            "otp": requested_otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_phone_otp_wrong_otp_unauthorized_400_fail(self):
        url = reverse("api-authentication:jwt-create-phone-otp")
        receiver = self.user_data.get("phone_number")

        requested_otp = "00000"

        data = {
            "receiver": receiver,
            "otp": requested_otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_create_email_authorized_200_ok(self):
        url = reverse("api-authentication:jwt-create-email")

        data = {
            "email": self.user_data.get("email"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_wrong_email_unauthorized_400_fail(self):
        url = reverse("api-authentication:jwt-create-email")
        wrong_email = "test13768212@faketest.com"

        data = {
            "email": wrong_email,
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_create_email_otp_authorized_200_ok(self):
        url = reverse("api-authentication:jwt-create-email-otp")
        receiver = self.user_data.get("email")

        requested_otp = generate_otp_for_receiver(receiver)
        self.assertIsNotNone(requested_otp, "Could'nt generate otp")

        data = {
            "receiver": receiver,
            "otp": requested_otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_email_wrong_otp_unauthorized_400_fail(self):
        url = reverse("api-authentication:jwt-create-email-otp")
        receiver = self.user_data.get("email")

        requested_otp = "01011"

        data = {
            "receiver": receiver,
            "otp": requested_otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_refresh_authorized_200_ok(self):
        login_url = reverse("api-authentication:jwt-create")
        refresh_url = reverse("api-authentication:jwt-refresh")

        login_data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        login_response = self.client.post(login_url, login_data)

        response_data = login_response.json()
        refresh_token = response_data.get("refresh")
        refresh_data = {
            "refresh": refresh_token,
        }

        refresh_response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)

    def test_jwt_refresh_unahtorized_401_fail(self):
        refresh_url = reverse("api-authentication:jwt-refresh")

        refresh_token = "fake_token"
        refresh_data = {
            "refresh": refresh_token,
        }

        refresh_response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(
            refresh_response.status_code, status.HTTP_401_UNAUTHORIZED
        )


class TokenAPITestCase(UserAPITestCase):
    def test_token_create_authorized_200_ok(self):
        url = reverse("api-authentication:token-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_create_unauthorized_401_fail(self):
        url = reverse("api-authentication:token-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("strong_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_authorized_200_ok(self):
        login_url = reverse("api-authentication:token-create")
        refresh_url = reverse("api-authentication:token-refresh")

        login_data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        login_response = self.client.post(login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        response_data = login_response.json()
        token = response_data.get("token")
        refresh_data = {
            "token": token,
        }

        refresh_response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)

    def test_token_refresh_unauthorized_401_fail(self):
        refresh_url = reverse("api-authentication:token-refresh")
        token = "fake_token"
        refresh_data = {
            "token": token,
        }

        refresh_response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(
            refresh_response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_token_verify_authorized_200_ok(self):
        login_url = reverse("api-authentication:token-create")
        verify_url = reverse("api-authentication:token-verify")

        login_data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        login_response = self.client.post(login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        response_data = login_response.json()
        token = response_data.get("token")
        verify_data = {
            "token": token,
        }

        verify_response = self.client.post(verify_url, verify_data)
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

    def test_token_verify_unauthorized_401_fail(self):
        verify_url = reverse("api-authentication:token-verify")

        token = "fake_token"
        verify_data = {
            "token": token,
        }

        verify_response = self.client.post(verify_url, verify_data)
        self.assertEqual(
            verify_response.status_code, status.HTTP_401_UNAUTHORIZED
        )
