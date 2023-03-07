from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user if he is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsOwner(permissions.BasePermission):
    """Allow users to edit their own categories"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UpdateOwnBooks(permissions.BasePermission):
    """Allow user to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class StaffPermission(permissions.BasePermission):
    edit_methods = ('PUT', 'PATCH', 'POST')
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff == True:
            return True
        return obj.user.is_staff == request.user.is_staff