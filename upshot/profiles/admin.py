from django.contrib import admin
from .models import Profile, ProfileAddress, ProfileEmail, ProfilePhoneNumber

# Register your models here.
from upshot.common.mixins import ModelAdminMixin


class ProfileEmailAdminStackedInline(admin.StackedInline):
    model = ProfileEmail
    fk_name = "profile"
    extra = 0
    readonly_fields = ["is_removed"]


class ProfilePhoneNumberAdminStackedInline(admin.StackedInline):
    model = ProfilePhoneNumber
    fk_name = "profile"
    extra = 0
    readonly_fields = ["is_removed"]


class ProfileAddressAdminStackedInline(admin.StackedInline):
    model = ProfileAddress
    fk_name = "profile"
    extra = 0
    readonly_fields = ["is_removed"]


@admin.register(Profile)
class ProfileAdminI(ModelAdminMixin):
    list_display = [
        "name",
        "user",
    ]

    readonly_fields = ["user", "is_removed"]

    inlines = [
        ProfileEmailAdminStackedInline,
        ProfilePhoneNumberAdminStackedInline,
        ProfileAddressAdminStackedInline,
    ]
