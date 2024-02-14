from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from upshot.profiles.api.mixins import ProfileFieldApiMixin


class JWTCreateProfilePasswordApiMixin(ProfileFieldApiMixin):
    def get_password(self):
        return self.profile_serializer.validated_data.get("password")

    def authenticate_user(self):
        password = self.get_password()
        user = self.get_profile_user()

        if user and password:
            authenticated_user = authenticate(
                username=user.username, password=password
            )
            return authenticated_user

        return None

    def get_tokens(self):
        authenticated_user = self.authenticate_user()
        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            }

        return {}

    def post(self, request, *args, **kwargs):
        self.validate_profile_serializer(request)
        tokens = self.get_tokens()
        if tokens:
            return Response(tokens, status=status.HTTP_200_OK)

        return Response(
            {"message": "User not found or Password is wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class JWTCreateProfileFieldOTPApiMixin(JWTCreateProfilePasswordApiMixin):
    def get_tokens(self):
        authenticated_user = self.get_profile_user()
        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            }

        return {}
