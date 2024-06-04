from django.contrib import admin

from .models import MentorRequest, MentorSetting


@admin.register(MentorRequest)
class MentorRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(MentorSetting)
class MentorSettingAdmin(admin.ModelAdmin):
    pass
