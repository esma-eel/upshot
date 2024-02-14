import unittest
from django.urls import reverse
from rest_framework import status
from upshot.common.tests.test_mixins import UserAPITestCase
from upshot.common.utils.otp_helpers import generate_otp_for_receiver


class OTPAPITestCase(UserAPITestCase):
    @unittest.skip("local-develop")
    def test_otp_phone_create_200_ok(self):
        url = reverse("api-common:otp-phone-create")

        data = {
            "phone_number": self.user_data.get("phone_number"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_otp_phone_create_503_fail(self):
        url = reverse("api-common:otp-phone-create")

        data = {
            "phone_number": self.user_data.get("phone_number"),
        }

        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def test_otp_phone_verify_200_ok(self):
        url = reverse("api-common:otp-phone-verify")
        receiver = self.user_data.get("phone_number")
        otp = generate_otp_for_receiver(receiver)

        data = {
            "receiver": receiver,
            "otp": otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_otp_phone_verify_400_fail(self):
        url = reverse("api-common:otp-phone-verify")
        receiver = self.user_data.get("phone_number")
        otp = "10101"

        data = {
            "receiver": receiver,
            "otp": otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @unittest.skip("local-develop")
    def test_otp_email_create_200_ok(self):
        url = reverse("api-common:otp-email-create")

        data = {
            "email": self.user_data.get("email"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_otp_email_create_503_fail(self):
        url = reverse("api-common:otp-email-create")

        data = {
            "email": self.user_data.get("email"),
        }

        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def test_otp_email_verify_200_ok(self):
        url = reverse("api-common:otp-email-verify")
        receiver = self.user_data.get("email")
        otp = generate_otp_for_receiver(receiver)

        data = {
            "receiver": receiver,
            "otp": otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_otp_email_verify_400_fail(self):
        url = reverse("api-common:otp-email-verify")
        receiver = self.user_data.get("email")
        otp = "01220"

        data = {
            "receiver": receiver,
            "otp": otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
