from rest_framework import serializers
from upshot.authentication.utils.password_helpers import (
    get_password_rules,
    check_password_strength,
    are_passwords_same,
)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()


class PasswordCheckSerializer(serializers.Serializer):
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate_password(self, value):
        is_strong_password = check_password_strength(value)

        if not is_strong_password:
            password_rules = get_password_rules()
            raise serializers.ValidationError({"password": password_rules})

        return value

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.get("repeat_password")
        are_same = are_passwords_same(password, repeat_password)

        if not are_same:
            raise serializers.ValidationError(
                {"message": "Passwords are not equal!"}
            )

        return attrs
