from rest_framework.serializers import ModelSerializer

from users.models import Payments, User


class PaymentsSerializer(ModelSerializer):
    """Класс-сериализатор для модели Платежи"""

    class Meta:
        model = Payments
        fields = "__all__"


class PaymentsRetrieveSerializer(ModelSerializer):
    """Класс-сериализатор для модели Платежи для просмотра платежа по session_id"""

    class Meta:
        model = Payments
        fields = "__all__"
        lookup_field = 'session_id'


class UserSerializer(ModelSerializer):
    """Класс-сериализатор для модели Пользователь"""

    class Meta:
        model = User
        fields = "__all__"


class UserDetailSerializer(ModelSerializer):
    """Класс-сериализатор для детального представления пользователя"""

    payments = PaymentsSerializer(source="payments_set", many=True)

    class Meta:
        model = User
        fields = "__all__"


class UserDetailRestUserSerializer(ModelSerializer):
    """Класс-сериализатор для детального представления пользователя для других остальных пользователей"""

    class Meta:
        model = User
        exclude = ('first_name', 'password')
