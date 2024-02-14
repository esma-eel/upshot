from rest_framework import serializers
from upshot.mentor.models import MentorSetting, MentorRequest


class MentorSettingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorSetting
        exclude = []
        read_only_fields = ["user"]


class MentorRequestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorRequest
        exclude = []
        read_only_fields = ["created", "user_from"]
