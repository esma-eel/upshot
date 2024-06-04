from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
)
from upshot.actions.models import Action
from upshot.account.models import User
from .serializers import ActionModelSerializer


class ActionModelViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Action.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ActionModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        following_ids = user.following.values_list("id", flat=True)
        all_users_except_request_user = User.objects.exclude(id=user.id)
        requested_user_actions = queryset.exclude(
            user__in=all_users_except_request_user
        )
        if user.is_superuser:
            return requested_user_actions

        if following_ids:
            actions = queryset.exclude(user=user)
            actions = actions.filter(user__id__in=following_ids)
            queryset = actions.select_related("user", "user__profile")
            return queryset

        return queryset.none()
