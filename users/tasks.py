from datetime import datetime, timedelta

import pytz
from celery import shared_task

from config import settings
from users.models import User


@shared_task
def execute_block_user():
    """ Блокирует пользователей, если пользователь не заходил более месяца """

    timezone = pytz.timezone(settings.TIME_ZONE)
    required_datetime = datetime.now(timezone) - timedelta(days=30)
    for user in User.objects.filter(last_login__lt=required_datetime, is_active=True):
        user.is_active = False
        user.save()
        print(f'User {user.email} blocked')
