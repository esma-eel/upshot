from django_filters import rest_framework as filters
from mentor.models import MentorSetting, MentorRequest


class MentorSettingFilterSet(filters.FilterSet):
    class Meta:
        model = MentorSetting
        exclude = []


class MentorRequestFilterSet(filters.FilterSet):
    class Meta:
        model = MentorRequest
        exclude = []
