from rest_framework import permissions


class PostPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Permission for CreateAPI view and ListAPI view.
        GET list of all posts by anyone.
        POST new post by Admin only.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        """
        Permission for RetrieveUpdateDestroyAPI View.
        GET a post by anyone.
        PUT, PATCH, DELETE a post by  Editor or Admin only.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff or request.user.is_superuser


class CommentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        GET all comments by anyone.
        POST by Authenticated User Only.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return (
                request.user.is_authenticated
                or request.user.is_staff
                or request.user.is_superuser
            )

    def has_object_permission(self, request, view, obj):
        """
        GET a comment by anyone.
        PUT / PATCH by Author Only.
        DELETE by Author or Super Admin or Editor.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == "PUT" or request.method == "PATCH":
            return obj.author == request.user
        elif request.method == "DELETE":
            return (
                obj.author == request.user
                or request.user.is_superuser
                or request.user.is_staff
            )


class LikePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        GET all likes by anyone.
        POST by Authenticated User Only.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        GET a like by anyone.
        PUT / PATCH by NO ONE.
        DELETE by Author or Super Admin only.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return obj.author == request.user or request.user.is_superuser
        else:
            return False


class PostHistoryPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        GET list of all Post Versions by Editor or Super Admin.
        POST is not allowed to anyone.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        GET a post's history by anyone.
        PUT / PATCH, DELETE not allowed by anyone.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
