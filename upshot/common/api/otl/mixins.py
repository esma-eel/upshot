from rest_framework.reverse import reverse
from upshot.common.utils.otl_helpers import (
    generate_otl_for_receiver,
    send_otl_to_receiver_email,
)
from upshot.profiles.api.mixins import ProfileEmailApiMixin


class RequestOTLApiMixin(ProfileEmailApiMixin):
    def generate_otl(self):
        receiver = self.get_profile_field_from_serializer()
        return generate_otl_for_receiver(receiver)

    def get_communication_function(self):
        return send_otl_to_receiver_email

    def send_otl(self):
        otl_value = self.generate_otl()
        receiver = self.get_profile_field_from_serializer()
        communication_function = self.get_communication_function()

        if otl_value:
            link = reverse(
                "api-authentication:reset-password-email-otl",
                args=[otl_value],
                request=self.request,
            )
            result = communication_function(receiver, link)
            return result

        return False
