from django_filters import rest_framework as filters
from upshot.account.models import Profile, User


class UserFilterSet(filters.FilterSet):
    class Meta:
        model = User
        exclude = []


class ProfileFilterSet(filters.FilterSet):
    class Meta:
        model = Profile
        exclude = ["photo"]
