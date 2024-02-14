from django.urls import reverse
from rest_framework import status
from upshot.common.tests.test_mixins import UserAPITestCase


class JWTBlackListAPITestCase(UserAPITestCase):
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
        return response.json()

    def subtest_refresh_blacklisted_token_unauthorized_401_fail(self):
        url: str = reverse("api-authentication:jwt-refresh")

        data = {"refresh": self.login_data.get("refresh")}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_blacklist_200_ok(self):
        url = reverse("api-authentication:jwt-blacklist")

        data = {"refresh": self.login_data.get("refresh")}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.subTest("check if refresh token is blacklisted"):
            self.subtest_refresh_blacklisted_token_unauthorized_401_fail()


class TokenBlackListAPITestCase(UserAPITestCase):
    def setUp(self):
        super().setUp()
        self.login_data = self.login()

    def login(self):
        url = reverse("api-authentication:token-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        return response.json()

    def subtest_refresh_blacklisted_token_unauthorized_401_fail(self):
        url: str = reverse("api-authentication:token-refresh")

        data = {"token": self.login_data.get("token")}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_blacklist_200_ok(self):
        url = reverse("api-authentication:token-blacklist")

        data = {"refresh": self.login_data.get("token")}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.subTest("check if refresh token is blacklisted"):
            self.subtest_refresh_blacklisted_token_unauthorized_401_fail()
