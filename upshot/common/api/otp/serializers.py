from upshot.common.utils.number_helpers import ir_phone_number
from upshot.common.utils.otp_helpers import verify_input_otp_of_receiver
from rest_framework import serializers


class OTPSerializer(serializers.Serializer):
    receiver = serializers.CharField()
    otp = serializers.CharField()

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                {"otp": "OTP Code format is wrong"}
            )

        return value

    def validate(self, attrs):
        receiver = attrs.get("receiver")
        otp = attrs.get("otp")

        is_verified = verify_input_otp_of_receiver(receiver, otp)

        if not is_verified:
            raise serializers.ValidationError(
                {"otp": "OTP Code is wrong or expired"}
            )

        return attrs


class PhoneOTPSerializer(OTPSerializer):
    receiver = serializers.CharField(max_length=11)
    otp = serializers.CharField()

    def validate_receiver(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value


class EmailOTPSerializer(OTPSerializer):
    receiver = serializers.EmailField()
    otp = serializers.CharField()
