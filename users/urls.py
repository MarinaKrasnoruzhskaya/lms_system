from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, PaymentsCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments-create'),

    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
]
