from rest_framework import status
from rest_framework.response import Response

from upshot.profiles.models import ProfilePhoneNumber, ProfileEmail
from .serializers import PhoneNumberSerializer, EmailSerializer


class ProfileFieldApiMixin:
    def get_profile_model(self):
        return None

    def get_profile_model_field_name(self):
        return ""

    def get_profile_serializer(self):
        return None

    def get_profile_serializer_field_name(self):
        return self.get_profile_model_field_name()

    def validate_profile_serializer(self, request):
        profile_serializer = self.get_profile_serializer()
        self.profile_serializer = profile_serializer(data=request.data)
        self.profile_serializer.is_valid(raise_exception=True)
        return self.profile_serializer

    def get_profile_field_from_serializer(self):
        serializer_field_name = self.get_profile_serializer_field_name()
        return self.profile_serializer.validated_data.get(serializer_field_name)

    def get_verified_profile_queryset(self):
        profile_model = self.get_profile_model()
        model_field_name = self.get_profile_model_field_name()
        field_value = self.get_profile_field_from_serializer()
        queryset = profile_model.objects.filter(
            is_primary=True,
            is_verified=True,
            **{model_field_name: field_value},
        )

        return queryset

    def get_queryset_field_only(self):
        profile_model = self.get_profile_model()
        model_field_name = self.get_profile_model_field_name()
        field_value = self.get_profile_field_from_serializer()
        queryset = profile_model.objects.filter(
            **{model_field_name: field_value},
        )

        return queryset

    def get_queryset(self):
        return self.get_verified_profile_queryset()

    def get_profile_field_object(self):
        queryset = self.get_queryset()
        if not queryset.exists():
            return None

        profile_field_object = queryset.last()
        return profile_field_object

    def get_profile_object(self):
        profile_field_object = self.get_profile_field_object()
        if profile_field_object:
            profile = profile_field_object.profile
            return profile
        return None

    def get_profile_user(self):
        profile_object = self.get_profile_object()
        if profile_object:
            profile_user = profile_object.user
            return profile_user

        return None


class ProfileFieldVerifyApiMixin(ProfileFieldApiMixin):
    def get_queryset(self):
        return self.get_queryset_field_only()

    def verify_field_object(self):
        field_object = self.get_profile_field_object()
        if not field_object:
            return False

        if not field_object.is_verified:
            field_object.is_verified = True
            field_object.save()

        return True

    def post(self, request, *args, **kwargs):
        self.validate_profile_serializer(request)
        is_verified = self.verify_field_object()
        field = self.get_profile_model_field_name()

        if not is_verified:
            return Response(
                {field: "does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "verified successfully"},
            status=status.HTTP_200_OK,
        )


class ProfilePhoneNumberApiMixin(ProfileFieldApiMixin):
    def get_profile_model(self):
        return ProfilePhoneNumber

    def get_profile_model_field_name(self):
        return "phone_number"

    def get_profile_serializer(self):
        return PhoneNumberSerializer

    def get_profile_serializer_field_name(self):
        return "phone_number"


class ProfileEmailApiMixin(ProfileFieldApiMixin):
    def get_profile_model(self):
        return ProfileEmail

    def get_profile_model_field_name(self):
        return "email"

    def get_profile_serializer(self):
        return EmailSerializer

    def get_profile_serializer_field_name(self):
        return "email"
