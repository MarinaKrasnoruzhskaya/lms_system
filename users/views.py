from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsListAPIView(ListAPIView):
    """ Класс-контроллер на основе базового класса дженерика для отображения списка платежей """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ('payment_date',)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')

