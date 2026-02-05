from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import UserSerializer, PaymentSerializer, UserRegisterSerializer
from .filters import PaymentFilter
from .permissions import IsModerator, IsOwner

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Все операции требуют авторизации

    def get_permissions(self):
        """ВСЕ методы требуют авторизации (регистрация через отдельный эндпоинт)."""
        return [permissions.IsAuthenticated()]


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для платежей с фильтрацией."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
