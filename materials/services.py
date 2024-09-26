from materials.models import Subscription


def get_list_email_subscript_user(course):
    """ Возвращает список email пользователей, подписанных на переданный course"""

    list_email = []

    for subscription in Subscription.objects.filter(course=course):
        list_email.append(subscription.user.email)

    return list_email
