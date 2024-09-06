from rest_framework.serializers import ModelSerializer

from users.models import Payments


class PaymentsSerializer(ModelSerializer):
    """ Класс-сериализатор для модели Платежи"""
    class Meta:
        model = Payments
        fields = '__all__'
