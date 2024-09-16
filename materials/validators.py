from rest_framework.serializers import ValidationError


def validate_link_to_video(value):
    """ Кастомный валидатор проверяет, что value является ссылкой на страницу с youtube.com, иначе вызывается ошибка """
    if 'youtube.com' not in value:
        raise ValidationError("Попытка использования ссылки на сторонние ресурсы")
