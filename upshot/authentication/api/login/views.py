from rest_framework.views import APIView

from upshot.common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from upshot.profiles.api.mixins import (
    ProfilePhoneNumberApiMixin,
    ProfileEmailApiMixin,
)
from .serializers import (
    EmailPasswordSerializer,
    PhonePasswordSerializer,
)
from .mixins import (
    JWTCreateProfilePasswordApiMixin,
    JWTCreateProfileFieldOTPApiMixin,
)


class JWTCreatePhonePasswordApiView(
    JWTCreateProfilePasswordApiMixin, ProfilePhoneNumberApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return PhonePasswordSerializer


class JWTCreateEmailPasswordApiView(
    JWTCreateProfilePasswordApiMixin, ProfileEmailApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return EmailPasswordSerializer


class JWTCreatePhoneOTPApiView(
    JWTCreateProfileFieldOTPApiMixin, ProfilePhoneNumberApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return PhoneOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"


class JWTCreateEmailOTPApiView(
    JWTCreateProfileFieldOTPApiMixin, ProfileEmailApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return EmailOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"
