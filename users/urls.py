from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, PaymentsCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView, \
    UserCreateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments-create'),

    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
