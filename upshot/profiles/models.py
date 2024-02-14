from django.db import models
from upshot.common.mixins import ModelMixin
from django.utils.translation import gettext_lazy as _
from .utils.upload_path import profile_upload


class ProfileEmail(ModelMixin):
    email = models.EmailField(_("Email"), unique=True)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    profile = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name="email_set"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(is_removed=False),
                name="unique_if_not_deleted_profile_email",
            )
        ]

    def __str__(self):
        return self.email


class ProfilePhoneNumber(ModelMixin):
    phone_number = models.CharField(
        _("Phone Number"), max_length=11, unique=True
    )
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    profile = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name="phone_number_set",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["phone_number"],
                condition=models.Q(is_removed=False),
                name="unique_if_not_deleted_profile_phone_number",
            )
        ]

    def __str__(self):
        return self.phone_number


class ProfileAddress(ModelMixin):
    city = models.CharField(_("City"), max_length=32, blank=True, null=True)
    address = models.TextField(_("Address"))
    is_primary = models.BooleanField(default=False)

    profile = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name="address_set",
    )

    def __str__(self):
        return f"{self.profile} Address"


class Profile(ModelMixin):
    name = models.CharField(_("Name"), max_length=32, blank=True, null=True)
    avatar = models.ImageField(
        _("Avatar"), blank=True, null=True, upload_to=profile_upload
    )

    user = models.OneToOneField(
        "users.User", on_delete=models.PROTECT, verbose_name=_("User")
    )

    def __str__(self):
        if self.name:
            return self.name

        return self.user.username

    def get_phone_numbers(self):
        return self.phone_number_set.all()

    def get_primary_phone_number(self):
        qs_phone_numbers = self.get_phone_numbers()
        qs_primary_phone_number = qs_phone_numbers.filter(is_primary=True)

        if qs_primary_phone_number.exists():
            return qs_primary_phone_number.last().phone_number

        return ""

    def get_emails(self):
        return self.email_set.all()

    def get_primary_email(self):
        qs_emails = self.get_emails()
        qs_primary_email = qs_emails.filter(is_primary=True)

        if qs_primary_email.exists():
            return qs_primary_email.last().email

        return ""
