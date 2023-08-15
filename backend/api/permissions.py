from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Предоставляет права запроса только автору объекта, в остальных случаях
    доступ запрещен."""

    def has_object_permission(self, request, view, object):
        return (
            request.method in permissions.SAFE_METHODS
            or object.author == request.user
        )
