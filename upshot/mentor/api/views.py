from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from upshot.mentor.models import MentorSetting, MentorRequest
from .serializers import (
    MentorSettingModelSerializer,
    MentorRequestModelSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsSenderOrReceiverOfMentorRequest
from .filters import MentorSettingFilterSet, MentorRequestFilterSet


class MentorSettingModelViewSet(ModelViewSet):

    http_method_names = [
        "get",
        "post",
        "patch",
    ]

    queryset = MentorSetting.objects.all()
    serializer_class = MentorSettingModelSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filterset_class = MentorSettingFilterSet

    lookup_field = "user__username"
    lookup_url_kwarg = "user__username"

    def perform_create(self, serializer):
        user = self.request.user
        try:
            return user.mentorsetting
        except MentorSetting.DoesNotExist:
            mentor_setting_object = serializer.save(user=user)
            return mentor_setting_object


class MentorRequestModelViewSet(ModelViewSet):
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]

    queryset = MentorRequest.objects.all().order_by("-created")
    serializer_class = MentorRequestModelSerializer
    permission_classes = [IsAuthenticated, IsSenderOrReceiverOfMentorRequest]
    filterset_class = MentorRequestFilterSet

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        owned_queryset = queryset.filter(Q(user_from=user) | Q(user_to=user))
        return owned_queryset

    def perform_create(self, serializer):
        mentor_request_object = serializer.save(user_from=self.request.user)
        return mentor_request_object

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user
        if user == instance.user_to:
            mentor_request_object = serializer.save()
            return mentor_request_object
        return None

    def perform_destroy(self, instance):
        user = self.request.user
        instance.approved = False
        instance.save()

        if user == instance.user_from:
            instance.delete()

        return None
