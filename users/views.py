from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer, extend_schema_view, OpenApiResponse
from rest_framework import filters, status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView, get_object_or_404,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payments, User
from users.permissions import IsProfile
from users.serializers import PaymentsSerializer, UserSerializer, UserDetailSerializer, UserDetailRestUserSerializer, \
    PaymentsRetrieveSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product, get_retrieve_session


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
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.payment_method == "card":
            product = create_stripe_product(payment)
            price = create_stripe_price(int(payment.payment_amount), product.name)
            session_id, payment_link = create_stripe_session(price)
            payment.session_id = session_id
            payment.link = payment_link
        payment.save()


class PaymentsRetrieveAPIView(RetrieveAPIView):
    """Класс-контроллер на основе базового класса дженерика для просмотра платежа по session_id"""

    serializer_class = PaymentsRetrieveSerializer
    queryset = Payments.objects.all()
    permission_classes = [AllowAny,]
    lookup_field = 'session_id'

    def get_object(self):
        """ Метод возвращает объект Queryset по переданному session_id """

        queryset = self.get_queryset()
        filter_dict = dict()
        filter_dict[self.lookup_field] = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, **filter_dict)
        if obj.payment_status != "complete":
            obj.payment_status = get_retrieve_session(obj.session_id)
            obj.save()
        return obj


class UserUpdateAPIView(UpdateAPIView):
    """Класс-контроллер на основе базового класса дженерика для редактирования пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsProfile]


@extend_schema_view(
    retrieve=extend_schema(
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description='Описание 500 ответа'),
        },
    ),
)
class UserRetrieveAPIView(RetrieveAPIView):
    """Класс-контроллер на основе базового класса дженерика для отображения одного пользователя"""

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        """ Метод возвращает объект Queryset по переданному pk """

        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        return queryset.first()

    # @extend_schema(responses={
    #     200: PolymorphicProxySerializer(
    #         component_name='User',
    #         serializers=[UserDetailSerializer, UserDetailRestUserSerializer],
    #         resource_type_field_name='pk',
    #     ),
    # })
    def get_serializer_class(self, *args, **kwargs):
        """ Метод предоставления сериализатор со всеми полями для своего профиля
        и сериализатор с общими полями для чужого профиля """

        if getattr(self, 'swagger_fake_view', False):  # drf-yasg comp
            return User.objects.none()
        if IsProfile().has_permission(self.request, self):
            serializer_class = UserDetailSerializer
        else:
            serializer_class = UserDetailRestUserSerializer
        return serializer_class


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
