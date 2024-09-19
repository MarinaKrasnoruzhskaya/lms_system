from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, PolymorphicProxySerializer
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payments, User
from users.permissions import IsProfile
from users.serializers import PaymentsSerializer, UserSerializer, UserDetailSerializer, UserDetailRestUserSerializer


class PaymentsListAPIView(ListAPIView):
    """Класс-контроллер на основе базового класса дженерика для отображения списка платежей"""

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ("payment_date",)
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")


class PaymentsCreateAPIView(CreateAPIView):
    """Класс-контроллер на основе базового класса дженерика для создания платежа"""

    serializer_class = PaymentsSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Класс-контроллер на основе базового класса дженерика для редактирования пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsProfile]


class UserRetrieveAPIView(RetrieveAPIView):
    """Класс-контроллер на основе базового класса дженерика для отображения одного пользователя"""

    queryset = User.objects.all()

    def get_queryset(self):
        """ Метод возвращает объект Queryset по переданному pk """

        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        return queryset

    def get_serializer_class(self, *args, **kwargs):
        """ Метод предоставления сериализатор со всеми полями для своего профиля
        и сериализатор с общими полями для чужого профиля """

        if IsProfile().has_permission(self.request, self):
            return UserDetailSerializer
        return UserDetailRestUserSerializer


class UserDestroyAPIView(DestroyAPIView):
    """Класс-контроллер на основе базового класса дженерика для удаления пользователя"""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateAPIView(CreateAPIView):
    """Класс-контроллер на основе базового класса дженерика для создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
