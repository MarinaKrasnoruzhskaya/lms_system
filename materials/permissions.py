from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Класс для определения, является ли авторизованный пользователь модератором"""

    def has_permission(self, request, view):
        """Метод для проверки принадлежности пользователя группе moderator"""
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(permissions.BasePermission):
    """ Класс для определения является ли авторизованный пользователь владельцем """

    def has_object_permission(self, request, view, obj):
        """ Метод для проверки является ли авторизованный пользователь владельцем """
        return obj.owner == request.user
