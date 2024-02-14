from rest_framework import status
from rest_framework.response import Response

from .serializers import PasswordCheckSerializer


class ChangePasswordApiMixin:
    def get_password_serializer(self):
        return PasswordCheckSerializer

    def validate_password_serializer(self, request):
        password_serializer = self.get_password_serializer()
        self.password_serializer = password_serializer(data=request.data)
        self.password_serializer.is_valid(raise_exception=True)
        return self.password_serializer

    def get_password(self):
        return self.password_serializer.validated_data.get("password")

    def get_user(self, **kwargs):
        return self.request.user

    def change_password(self):
        user_obj = self.get_user()
        if user_obj:
            password_value = self.get_password()
            user_obj.set_password(password_value)
            user_obj.save()
            return True

        return False

    def post(self, request, *args, **kwargs):
        self.validate_password_serializer(request)
        is_changed = self.change_password()
        if is_changed:
            return Response(
                data={"message": "Password changed"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"message": "Could'nt change password, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )
