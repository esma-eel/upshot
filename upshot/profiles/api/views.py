from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from upshot.common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from .mixins import (
    ProfilePhoneNumberApiMixin,
    ProfileEmailApiMixin,
    ProfileFieldVerifyApiMixin,
)

from .serializers import (
    ProfileModelSerializer,
)
from upshot.profiles.models import Profile


class VerifyPhoneNumberWithOTPView(
    ProfileFieldVerifyApiMixin,
    ProfilePhoneNumberApiMixin,
    APIView,
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return PhoneOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"


class VerifyEmailWithOTPView(
    ProfileFieldVerifyApiMixin,
    ProfileEmailApiMixin,
    APIView,
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return EmailOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"


class RetrieveUpdateProfileAPIView(RetrieveUpdateAPIView):
    allowed_methods = ["get", "patch"]
    http_method_names = ["get", "patch"]

    permission_classes = []

    serializer_class = ProfileModelSerializer
    lookup_field = "user__username"

    queryset = Profile.objects.all()
