from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from mentor.models import MentorSetting, MentorRequest
from .serializers import (
    MentorSettingModelSerializer,
    MentorRequestModelSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsSenderOrReceiverOfMentorRequest
from .filters import MentorSettingFilterSet, MentorRequestFilterSet


class MentorSettingModelViewSet(ModelViewSet):
    queryset = MentorSetting.objects.all()
    serializer_class = MentorSettingModelSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = MentorSettingFilterSet

    def perform_create(self, serializer):
        mentor_setting_object = serializer.save(user=self.request.user)
        return mentor_setting_object


class MentorRequestModelViewSet(ModelViewSet):
    queryset = MentorRequest.objects.all().order_by("-created")
    serializer_class = MentorRequestModelSerializer
    permission_classes = [IsSenderOrReceiverOfMentorRequest]
    filterset_class = MentorRequestFilterSet

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        owned_queryset = queryset.filter(Q(user_from=user) | Q(user_to=user))
        return owned_queryset

    def perform_create(self, serializer):
        mentor_request_object = serializer.save(user_from=self.request.user)
        return mentor_request_object

    def perform_destroy(self, instance):
        user = self.request.user
        if user == instance.user_from:
            instance.delete()

        instance.approved = False
        instance.save()
