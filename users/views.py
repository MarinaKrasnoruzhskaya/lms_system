from rest_framework.generics import ListAPIView

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsListAPIView(ListAPIView):
    """ Класс-контроллер на основе базового класса дженерика для отображения списка платежей """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
