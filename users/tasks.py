from celery import shared_task

from users.models import User
from users.services import get_required_datetime


@shared_task
def execute_block_user():
    """ Блокирует пользователей, если пользователь не заходил более месяца """

    required_datetime = get_required_datetime(hours=0, days=30)
    for user in User.objects.filter(last_login__lt=required_datetime):
        print(user.email)
        user.is_active = False
        user.save()
        print(f'User {user.email} blocked')
