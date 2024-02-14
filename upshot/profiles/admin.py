from django.contrib import admin
from .models import Profile

from upshot.common.mixins import ModelAdminMixin


@admin.register(Profile)
class ProfileAdmin(ModelAdminMixin):
    pass
