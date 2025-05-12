from rest_framework.permissions import BasePermission


class IsGuest(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        return token and token.get('guest') is True
