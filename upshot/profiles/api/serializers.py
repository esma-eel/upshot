from django.db import transaction
from upshot.common.utils.number_helpers import ir_phone_number
from rest_framework import serializers
from upshot.profiles.models import (
    ProfilePhoneNumber,
    ProfileEmail,
    ProfileAddress,
    Profile,
)


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ProfilePhoneNumberModelSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, validators=[])

    class Meta:
        model = ProfilePhoneNumber
        fields = [
            "id",
            "phone_number",
            "is_primary",
            "is_verified",
        ]
        extra_kwargs = {
            "is_primary": {
                "required": True,
                "allow_null": False,
            },
            "is_verified": {"read_only": True},
            "id": {"read_only": False, "required": False},
        }

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value


class ProfileEmailModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = ProfileEmail
        fields = [
            "id",
            "email",
            "is_primary",
            "is_verified",
        ]
        extra_kwargs = {
            "is_primary": {
                "required": True,
                "allow_null": False,
            },
            "is_verified": {"read_only": True},
            "id": {"read_only": False, "required": False},
        }


class ProfileAddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAddress
        fields = [
            "id",
            "city",
            "address",
            "is_primary",
        ]
        extra_kwargs = {
            "is_primary": {
                "required": True,
                "allow_null": False,
            },
            "id": {"read_only": False, "required": False},
        }


class ProfileModelSerializer(serializers.ModelSerializer):
    phone_numbers = ProfilePhoneNumberModelSerializer(
        source="phone_number_set",
        many=True,
        required=False,
    )
    emails = ProfileEmailModelSerializer(
        source="email_set",
        many=True,
        required=False,
    )
    addresses = ProfileAddressModelSerializer(
        source="address_set",
        many=True,
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            "name",
            "avatar",
            "phone_numbers",
            "emails",
            "addresses",
        ]
        extra_kwargs = {
            "name": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        # pop nested data from original validated_data
        # in order to first create the main object which we need it
        validated_data_no_nested = validated_data.copy()
        for key, value in self.get_fields().items():
            if isinstance(value, serializers.ListSerializer):
                kname = value.source if value.source is not None else key
                validated_data_no_nested.pop(kname, None)

        # create main object based on default creation
        main_obj = super().create(validated_data_no_nested)

        # create nested related objects like reminders for todo
        for key, value in self.get_fields().items():
            if isinstance(value, serializers.ListSerializer):
                items = validated_data.pop(
                    value.source if value.source is not None else key, None
                )
                if items is not None:
                    ItemModel = value.child.Meta.model
                    link_field = None
                    for field in ItemModel._meta.fields:
                        if field.related_model == self.Meta.model:
                            link_field = field.name

                    if link_field is not None:
                        for item in items:
                            item[link_field] = main_obj
                            ItemModel.objects.create(**item)

        return main_obj

    @transaction.atomic
    def update(self, instance, validated_data):
        # pop nested data from original validated_data
        # in order to first create the main object which we need it
        validated_data_no_nested = validated_data.copy()
        for key, value in self.get_fields().items():
            if isinstance(value, serializers.ListSerializer):
                kname = value.source if value.source is not None else key
                validated_data_no_nested.pop(kname, None)

        # create main object based on default creation
        main_obj = super().update(instance, validated_data_no_nested)

        # create nested related objects like reminders for todo
        for key, value in self.get_fields().items():
            if isinstance(value, serializers.ListSerializer):
                items = validated_data.pop(
                    value.source if value.source is not None else key, None
                )
                if items is not None:
                    ItemModel = value.child.Meta.model
                    link_field = None
                    for field in ItemModel._meta.fields:
                        if field.related_model == self.Meta.model:
                            link_field = field.name

                    if link_field is not None:
                        for item in items:
                            item[link_field] = main_obj
                            try:
                                if item.get("id"):
                                    qs = ItemModel.objects.filter(id=item["id"])
                                    if qs.exists():
                                        item_obj = qs.last()
                                        for attr, value in item.items():
                                            setattr(item_obj, attr, value)
                                        item_obj.save()
                                else:
                                    ItemModel.objects.create(**item)
                            except Exception as e:
                                raise serializers.ValidationError({key: str(e)})

        return main_obj
