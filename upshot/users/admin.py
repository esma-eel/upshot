from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from upshot.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (_("Pesonal Information"), {"fields": ["name", "edit_profile"]}),
        (_("Authentication"), {"fields": ("username", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "username",
        "is_staff",
        "is_superuser",
    ]
    search_fields = [
        "username",
    ]
    readonly_fields = [
        "name",
        "edit_profile",
        "last_login",
        "date_joined",
        "is_superuser",
    ]

    def name(self, obj):
        if hasattr(obj, "profile"):
            if obj.profile.name:
                return obj.profile.name
        return "-"

    def edit_profile(self, obj):
        if not hasattr(obj, "profile"):
            return "-"

        link = reverse("admin:profiles_profile_change", args=[obj.profile.id])
        return format_html(f'<a class="button" href="{link}">Edit Profile</a>')
