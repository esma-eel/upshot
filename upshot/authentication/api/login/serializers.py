# from rest_framework import serializers
from upshot.profiles.api.serializers import (
    PhoneNumberSerializer,
    EmailSerializer,
)
from upshot.authentication.api.password.serializers import (
    PasswordSerializer,
)


class PhonePasswordSerializer(PhoneNumberSerializer, PasswordSerializer):
    pass


class EmailPasswordSerializer(EmailSerializer, PasswordSerializer):
    pass
