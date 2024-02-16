import copy
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.decorators import action
from upshot.account.models import User, Contact, Profile
from .serializers import (
    ContactModelSerializer,
    UserModelSerializer,
    CreateUserModelSerializer,
    ProfileModelSerializer,
    PasswordCheckSerializer,
)
from .filters import UserFilterSet, ProfileFilterSet, ContactFilterSet
from .permissions import (
    IsStaffUser,
    IsOwnerOrReadOnlyOfProfile,
    IsOwnerOrReadOnlyOfUser,
    IsSenderOrReceiverOfContact,
)


class UserModelViewSet(ModelViewSet):
    http_method_names = [
        "get",
        "post",
        "patch",
    ]
    serializer_class = UserModelSerializer
    create_serializer_class = CreateUserModelSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = UserFilterSet
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_serializer_class(self):
        if self.action in ["create", "register_user"]:
            return self.create_serializer_class

        return self.serializer_class

    def get_permissions(self):
        # specify permission for each mehtod
        action = self.action
        if action in ["update", "partial_update"]:
            self.permission_classes.append(IsOwnerOrReadOnlyOfUser)
        elif action in ["create"]:
            self.permission_classes.append(IsStaffUser)
        elif action in ["register_user"]:
            self.permission_classes = []

        return super().get_permissions()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.create_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = copy.deepcopy(serializer.validated_data)
        authentication_data = serializer_data.pop("authentication")

        authentication_serializer = PasswordCheckSerializer(
            data=authentication_data
        )
        authentication_serializer.is_valid(raise_exception=True)

        user_data = serializer_data.pop("user")
        profile_data = serializer_data.pop("profile")

        user_serializer = UserModelSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_object = user_serializer.save()

        profile_serializer = ProfileModelSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save(user=user_object)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {"user": user_data, "profile": profile_data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        serializer_class=create_serializer_class,
        permission_classes=[],
    )
    def register_user(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProfileModelViewSet(ModelViewSet):
    http_method_names = [
        "get",
        "post",
        "patch",
    ]
    serializer_class = ProfileModelSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyOfProfile]
    filterset_class = ProfileFilterSet
    lookup_field = "user__username"
    lookup_url_kwarg = "user__username"

    def perform_create(self, serializer):
        user = self.request.user
        try:
            return user.profile
        except Profile.DoesNotExist:
            profile = serializer.save(user=user)
            return profile


class ContactModelViewSet(ModelViewSet):
    http_method_names = [
        "get",
        "post",
        "delete",
    ]

    queryset = Contact.objects.all().order_by("-created")
    serializer_class = ContactModelSerializer
    permission_classes = [IsAuthenticated, IsSenderOrReceiverOfContact]
    filterset_class = ContactFilterSet

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        owned_queryset = queryset.filter(Q(user_from=user) | Q(user_to=user))
        return owned_queryset

    def perform_create(self, serializer):
        contact_request_object = serializer.save(user_from=self.request.user)
        return contact_request_object
