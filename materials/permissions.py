from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Класс для определения, является ли пользователь модератором"""

    def has_permission(self, request, view):
        """Метод для проверки принадлежности пользователя группе moderator"""
        return request.user.groups.filter(name="moderator").exists()
