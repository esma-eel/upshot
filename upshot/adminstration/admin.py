from django.contrib import admin
from upshot.common.mixins import ModelAdminMixin
from .models import APIKey


@admin.register(APIKey)
class APIKeyModelAdmin(ModelAdminMixin):
    list_display = [
        "id",
        "name",
        "code",
        "description",
    ]

    search_fields = ["name", "code", "description"]
