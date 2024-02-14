# from django.urls import reverse
# from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from upshot.profiles.models import (
    ProfilePhoneNumber,
    ProfileEmail,
    ProfileAddress,
)

User = get_user_model()


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "name": "Test User",
            "username": "test_user",
            "email": "test_email@test.com",
            "phone_number": "09121234579",
            "weak_password": "test_password",
            "strong_password": "W34el@come",
            "city": "Karaj",
            "address": "just address",
        }
        self.user = User.objects.create(
            username=self.user_data.get("username"),
        )
        self.user.set_password(self.user_data.get("weak_password"))
        self.user.save()
        self.user_profile = self.user.profile

        self.profile_phone = ProfilePhoneNumber.objects.create(
            is_primary=True,
            is_verified=True,
            phone_number=self.user_data.get("phone_number"),
            profile=self.user_profile,
        )

        self.profile_email = ProfileEmail.objects.create(
            is_primary=True,
            is_verified=True,
            email=self.user_data.get("email"),
            profile=self.user_profile,
        )

        self.profile_address = ProfileAddress.objects.create(
            is_primary=True,
            city=self.user_data.get("city"),
            address=self.user_data.get("address"),
            profile=self.user_profile,
        )

    def tearDown(self):
        # just for more information
        self.user_profile.delete()
        self.user.delete()

        return super().tearDown()
