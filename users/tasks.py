from datetime import datetime, timedelta

from celery import shared_task

from users.models import User


@shared_task
def execute_block_user():
    """ Блокирует пользователей, если пользователь не заходил более месяца """

    required_datetime = datetime.now() - timedelta(days=39)
    for user in User.objects.filter(last_login__lt=required_datetime):
        user.is_active = False
        user.save()
        print(f'User {user.email} blocked')
