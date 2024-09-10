from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer, UserDetailSerializer


class PaymentsListAPIView(ListAPIView):
    """ Класс-контроллер на основе базового класса дженерика для отображения списка платежей """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ('payment_date',)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')


class PaymentsCreateAPIView(CreateAPIView):
    """ Класс-контроллер на основе базового класса дженерика для создания платежа """
    serializer_class = PaymentsSerializer


class UserUpdateAPIView(UpdateAPIView):
    """ Класс-контроллер на основе базового класса дженерика для редактирования пользователя """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """ Класс-контроллер на основе базового класса дженерика для отображения одного пользователя """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserDestroyAPIView(DestroyAPIView):
    """ Класс-контроллер на основе базового класса дженерика для удаления пользователя """
    queryset = User.objects.all()


class UserCreateAPIView(CreateAPIView):
    """ Класс-контроллер на основе базового класса дженерика для создания пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
