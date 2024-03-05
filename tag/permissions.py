from rest_framework import permissions

class TagsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        ListCreate View Permissions.
        Allows any GET permission.
        POST permissions for Super Admin (Superuser)
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        """
        Retrieve, 
        Allows any GET permission.
        POST, PUT, PATCH permissions for Super Admin (Superuser)
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser