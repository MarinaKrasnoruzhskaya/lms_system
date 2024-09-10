from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Класс для кастомной команды создания суперпользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(email="admin@lms.com")
        user.set_password("admin")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        user = User.objects.create(email="user_1@lms.com")
        user.set_password("123456")
        user.is_active = True
        user.save()

        user = User.objects.create(email="user_2@lms.com")
        user.set_password("123456")
        user.is_active = True
        user.save()
