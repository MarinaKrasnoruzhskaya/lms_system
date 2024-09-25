from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Course, Subscription


@shared_task
def send_mail_update_course(pk_course):
    """ Отправляет сообщение пользователям, подписанным на обновление курса по переданному pk курса """

    course = Course.objects.get(id=pk_course)

    send_mail(
        subject=f"Обновление курса {course.title}",
        message=f"Курс {course.title} обновлен",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=get_list_email_subscript_user(course),
        fail_silently=False,
    )
    print('письмо отпрввлено')


def get_list_email_subscript_user(course):
    """ Возвращает список email пользователей, подписанных на переданный course"""

    list_email = []

    for subscription in Subscription.objects.filter(course=course):
        list_email.append(subscription.user.email)
    print(list_email)
    return list_email
