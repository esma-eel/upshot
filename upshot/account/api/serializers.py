from rest_framework import serializers
from upshot.account.models import User, Profile, Contact
from upshot.utils.password_helpers import (
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


class ProfileModelSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if self.instance:
            # update
            for create_only_field in self.Meta.create_only_fields:
                if create_only_field in data.keys():
                    data.pop(create_only_field)
        return data

    class Meta:
        model = Profile
        fields = [
            "grade",
            "student_number",
            "photo",
            "about",
        ]
        create_only_fields = ["user"]


class UserModelSerializer(serializers.ModelSerializer):
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "profile"]
        read_only_fields = ["profile"]


class CreateUserModelSerializer(serializers.Serializer):
    user = UserModelSerializer()
    profile = ProfileModelSerializer()
    authentication = PasswordCheckSerializer()


class ContactModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ["created"]
