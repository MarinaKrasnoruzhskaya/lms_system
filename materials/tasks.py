from datetime import datetime, timedelta

import pytz
from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Course, Lesson
from materials.services import get_list_email_subscript_user


@shared_task
def send_mail_update_course(pk_course):
    """ Проверяет, что последнее обновление курса или уроков курса было не менее 4 часов назад и отправляет сообщение
    пользователям, подписанным на обновление курса, по переданному pk курса """

    course = Course.objects.get(id=pk_course)
    lesson = Lesson.objects.filter(course=course).order_by('-updated_at').first()

    timezone = pytz.timezone(settings.TIME_ZONE)
    datetime_now = datetime.now(timezone)
    period = timedelta(hours=4)

    if (datetime_now - lesson.updated_at >= period) and (datetime_now - course.updated_at >= period):
        send_mail(
            subject=f"Обновление курса {course.title}",
            message=f"Курс {course.title} обновлен",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=get_list_email_subscript_user(course),
            fail_silently=False,
        )
        print('письмо отправлено')
    else:
        print('письмо не отправлено')
