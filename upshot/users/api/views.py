import copy
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db import transaction
from upshot.profiles.api.serializers import ProfileModelSerializer
from .serializers import (
    CreateUserModelSerializer,
    UserModelSerializer,
    RegisterUserSerilaizer,
)

User = get_user_model()


class UserCreateAPIView(APIView):
    serializer_class = CreateUserModelSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def profile_update(self, user_object, profile_data):
        profile_object = user_object.profile
        serializer = ProfileModelSerializer(
            instance=profile_object, data=profile_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        profile_object = serializer.save()
        return profile_object

    def authentication_set(self, user_object, authenticate_data):
        password = authenticate_data.get("password")
        user_object.set_password(password)
        user_object.save()
        return user_object

    def user_create(self, user_data):
        profile_data = user_data.pop("profile")
        user_object = User.objects.create(**user_data)
        self.profile_update(user_object, profile_data)
        return user_object

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = copy.deepcopy(serializer.data)
        user_data = serializer_data.pop("user")
        authentication_data = serializer_data.pop("authentication")

        user_object = self.user_create(user_data)
        self.authentication_set(user_object, authentication_data)

        created_serializer = UserModelSerializer(instance=user_object)

        return Response(
            created_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UserRegisterAPIView(UserCreateAPIView):
    serializer_class = RegisterUserSerilaizer
    allowed_methods = ["post"]
    http_method_names = ["post"]

    permission_classes = []
    authentication_classes = []

    def generate_user_data(self, serializer_data):
        user_data = {
            "username": serializer_data.get("username"),
            "profile": {
                "name": serializer_data.get("name"),
                "phone_numbers": [
                    {
                        "phone_number": serializer_data.get("phone_number"),
                        "is_primary": True,
                    },
                ],
                "emails": [
                    {
                        "email": serializer_data.get("email"),
                        "is_primary": True,
                    }
                ],
            },
        }
        return user_data

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = copy.deepcopy(serializer.data)

        authentication_data = serializer_data.pop("authentication")
        user_data = self.generate_user_data(serializer_data)

        validated_data = {
            "user": copy.deepcopy(user_data),
            "authentication": copy.deepcopy(authentication_data),
        }
        validate_serializer = CreateUserModelSerializer(data=validated_data)
        validate_serializer.is_valid(raise_exception=True)

        user_object = self.user_create(user_data)
        self.authentication_set(user_object, authentication_data)

        created_serializer = UserModelSerializer(instance=user_object)
        headers = self.get_success_headers(request.data)

        return Response(
            created_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
