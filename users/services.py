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
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
