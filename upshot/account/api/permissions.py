from rest_framework import permissions


class IsOwnerOrReadOnlyOfUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj == request.user


class IsOwnerOrReadOnlyOfProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSenderOrReceiverOfContact(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user_from == request.user or obj.user_to == request.user
