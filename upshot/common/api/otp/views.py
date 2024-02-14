from rest_framework.views import APIView

from upshot.common.utils.otp_helpers import (
    send_otp_to_receiver_sms,
    send_otp_to_receiver_email,
)

from .serializers import EmailOTPSerializer, PhoneOTPSerializer
from .mixins import VerifyOTPApiMixin, RequestOTPApiMixin
from upshot.profiles.api.mixins import (
    ProfilePhoneNumberApiMixin,
    ProfileEmailApiMixin,
)


class RequestOTPPhoneApiView(
    RequestOTPApiMixin, ProfilePhoneNumberApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_communication_function(self):
        return send_otp_to_receiver_sms


class RequestOTPEmailApiView(RequestOTPApiMixin, ProfileEmailApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_communication_function(self):
        return send_otp_to_receiver_email


class VerifyOTPPhoneApiView(VerifyOTPApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_otp_serialzier(self):
        return PhoneOTPSerializer


class VerifyOTPEmailApiView(VerifyOTPApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_otp_serialzier(self):
        return EmailOTPSerializer
