from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPostOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsCommentOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff


class IsLikeOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.owner()
