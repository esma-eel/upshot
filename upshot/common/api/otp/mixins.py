from rest_framework import status
from rest_framework.response import Response

from upshot.common.utils.otp_helpers import generate_otp_for_receiver

from upshot.profiles.api.mixins import ProfileFieldApiMixin


class RequestOTPApiMixin(ProfileFieldApiMixin):
    def generate_otp(self):
        receiver = self.get_profile_field_from_serializer()
        return generate_otp_for_receiver(receiver)

    def get_communication_function(self):
        return None

    def send_otp(self):
        otp_value = self.generate_otp()
        receiver = self.get_profile_field_from_serializer()
        communication_function = self.get_communication_function()

        if otp_value:
            result = communication_function(receiver, otp_value)
            return result

        return False

    def post(self, request, *args, **kwargs):
        self.validate_profile_serializer(request)
        otp_sent = self.send_otp()

        if not otp_sent:
            return Response(
                data={"message": "OTP Service is down, try later"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            data={"message": "OTP Sent"},
            status=status.HTTP_200_OK,
        )


class VerifyOTPApiMixin:
    def get_otp_serialzier(self):
        return None

    def validate_otp_serializer(self, request):
        serializer = self.get_otp_serialzier()
        self.otp_serializer = serializer(data=request.data)
        self.otp_serializer.is_valid(raise_exception=True)
        return self.otp_serializer

    def post(self, request, *args, **kwargs):
        self.validate_otp_serializer(request)
        return Response(
            data={"message": "OK!"},
            status=status.HTTP_200_OK,
        )
