from django.urls import reverse
from rest_framework import status
from upshot.common.tests.test_mixins import UserAPITestCase
from upshot.common.utils.otp_helpers import generate_otp_for_receiver


class VerifyProfileFieldAPITestCase(UserAPITestCase):
    def test_verify_phone_number_otp_200_ok(self):
        url = reverse("api-profiles:profile-verify-phone")
        receiver = self.user_data.get("phone_number")
        otp = generate_otp_for_receiver(receiver)

        data = {
            "receiver": receiver,
            "otp": otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_phone_number_otp_wrong_phone_number_400_fail(self):
        url = reverse("api-profiles:profile-verify-phone")
        receiver = "09123980342"
        otp = generate_otp_for_receiver(receiver)

        data = {
            "receiver": receiver,
            "otp": otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_otp_200_ok(self):
        url = reverse("api-profiles:profile-verify-email")
        receiver = self.user_data.get("email")
        otp = generate_otp_for_receiver(receiver)

        data = {
            "receiver": receiver,
            "otp": otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_email_otp_wrong_email_400_fail(self):
        url = reverse("api-profiles:profile-verify-email")
        receiver = "fakeemail@em.com"
        otp = generate_otp_for_receiver(receiver)

        data = {
            "receiver": receiver,
            "otp": otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
