from rest_framework import permissions


class IsProfile(permissions.BasePermission):
    """Класс для определения соответствия профиля авторизованному пользователю """

    def has_permission(self, request, view):
        """Метод для проверки соответствия профиля и авторизованного пользователя"""
        return request.user.pk == request.parser_context['kwargs']['pk']
