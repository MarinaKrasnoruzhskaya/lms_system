from datetime import datetime, timedelta

import pytz
import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(instance):
    """ Создает продукт в страйпе """
    if instance.paid_course:
        name = instance.paid_course
    else:
        name = instance.paid_lesson
    return stripe.Product.create(name=name)


def create_stripe_price(amount, name):
    """ Создает цену в страйпе """

    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": name},
    )


def create_stripe_session(price):
    """ Создает сессию оплаты в страйпе """

    session = stripe.checkout.Session.create(
        success_url='http://localhost:8000/' + 'users/payments/{CHECKOUT_SESSION_ID}',
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def get_retrieve_session(id_session):
    """ Получает информацию о сессии оплаты в страйпе """

    session = stripe.checkout.Session.retrieve(id_session)
    return session.get('status')


def get_required_datetime(hours=0, days=0):
    """ Возвращает объект Datetime, полученный в результаты разницы текущей даты и переданных значений hours и days"""

    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    required_datetime = current_datetime - timedelta(hours=hours, days=days)
    return required_datetime
