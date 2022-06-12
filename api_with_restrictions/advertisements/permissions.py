from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permmisions(self, request, view, obj):
        return request.User == obj.User
