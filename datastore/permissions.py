from rest_framework import permissions

class OwnerPermissionStore(permissions.BasePermission):
    """
    Object-level permission to only allow owener
    """
    def has_object_permission(self, request, view, obj):
        return obj.company.manager.user.id == request.user.id
