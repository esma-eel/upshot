from rest_framework import serializers
from upshot.common.utils.otl_helpers import verify_input_otl_of_receiver


class EmailAndOTLSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otl = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        otl = attrs.get("otl")

        result = verify_input_otl_of_receiver(otl, email)

        if not result:
            raise serializers.ValidationError(
                {"otl": "OTL Token is wrong or expired"}
            )

        return attrs
