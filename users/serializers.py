from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'city']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            city=validated_data.get('city', '')
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения пользователя."""

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar']
        read_only_fields = ['id']


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей."""

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']
        read_only_fields = ['payment_date']