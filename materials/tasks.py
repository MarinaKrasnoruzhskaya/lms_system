from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Course, Subscription, Lesson
from materials.services import is_difference_datetime


@shared_task
def send_mail_update_course(pk_course):
    """ Отправляет сообщение пользователям, подписанным на обновление курса по переданному pk курса """

    course = Course.objects.get(id=pk_course)
    lesson = Lesson.objects.filter(course=course).order_by('-updated_at').first()

    if is_difference_datetime(lesson.updated_at, hours=0.5) and is_difference_datetime(course.updated_at, hours=0.5):
        send_mail(
            subject=f"Обновление курса {course.title}",
            message=f"Курс {course.title} обновлен",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=get_list_email_subscript_user(course),
            fail_silently=False,
        )
        print('письмо отправлено')
    print('письмо не отправлено')


def get_list_email_subscript_user(course):
    """ Возвращает список email пользователей, подписанных на переданный course"""

    list_email = []

    for subscription in Subscription.objects.filter(course=course):
        list_email.append(subscription.user.email)

    return list_email
