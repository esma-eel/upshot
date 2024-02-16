from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import Contact, Profile, User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
