from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Retrieve user role safely (defaulting to standard)
        user_role = getattr(getattr(request.user, "profile", None), "role", "standard")
        return user_role == "admin" or obj.user == request.user
