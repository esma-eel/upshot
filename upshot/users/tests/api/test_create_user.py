import copy
from django.urls import reverse
from rest_framework import status
from upshot.common.tests.test_mixins import UserAPITestCase


class CreateUserAPITestCase(UserAPITestCase):
    def setUp(self):
        super().setUp()
        self.login_data = self.login()

        self.create_user_data = {
            "user": {
                "username": "testuser125",
                "profile": {
                    "name": "hello",
                    "phone_numbers": [
                        {"phone_number": "09120001480", "is_primary": True}
                    ],
                    "emails": [
                        {"email": "veryemailshit@gm.com", "is_primary": True}
                    ],
                    "addresses": [],
                },
            },
            "authentication": {
                "password": "1234@Esmaeel",
                "repeat_password": "1234@Esmaeel",
            },
        }

        self.register_user_data = {
            "username": "testuser130",
            "name": "hello",
            "phone_number": "09120001482",
            "email": "test@fakewkea6aaa.com",
            "authentication": {
                "password": "1234@Esmaeel",
                "repeat_password": "1234@Esmaeel",
            },
        }

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

    def test_create_user_by_staff_201_created(self):
        url = reverse("api-users:user-create")
        self.authenticate_client()
        response = self.client.post(url, self.create_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_by_anon_user_403_fail(self):
        url = reverse("api-users:user-create")
        response = self.client.post(url, self.create_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user_201_created(self):
        url = reverse("api-users:user-register")
        self.authenticate_client()
        response = self.client.post(url, self.register_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_repeated_data_400_fail(self):
        with self.subTest():
            self.test_create_user_by_staff_201_created()

        url = reverse("api-users:user-register")
        data = copy.deepcopy(self.register_user_data)

        data["email"] = self.create_user_data["user"]["profile"]["emails"][0][
            "email"
        ]
        data["phone_number"] = self.create_user_data["user"]["profile"][
            "phone_numbers"
        ][0]["phone_number"]

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
