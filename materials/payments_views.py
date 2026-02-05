# materials/payments_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Course
from users.models import Payment
from .services import create_stripe_product, create_stripe_price, create_stripe_session


class CreatePaymentAPIView(APIView):
    """
    API для создания платежа за курс.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создать платеж за курс",
        manual_parameters=[
            openapi.Parameter(
                "course_id",
                openapi.IN_QUERY,
                description="ID курса для оплаты",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "session_id": openapi.Schema(type=openapi.TYPE_STRING),
                    "url": openapi.Schema(type=openapi.TYPE_STRING),
                    "payment_status": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            400: "Некорректные данные",
            404: "Курс не найден",
        },
    )
    def post(self, request):
        course_id = request.data.get("course_id") or request.query_params.get(
            "course_id"
        )

        if not course_id:
            return Response(
                {"error": "Не указан course_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # Создаем продукт в Stripe
        product_id = create_stripe_product(course)
        if not product_id:
            return Response(
                {"error": "Ошибка создания продукта в платежной системе"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Создаем цену в Stripe
        price_id = create_stripe_price(course, product_id)
        if not price_id:
            return Response(
                {"error": "Ошибка создания цены в платежной системе"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Создаем сессию оплаты в Stripe
        session_data = create_stripe_session(price_id, course.id, user.email)
        if not session_data:
            return Response(
                {"error": "Ошибка создания сессии оплаты"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Создаем запись о платеже в нашей системе
        payment = Payment.objects.create(
            user=user,
            paid_course=course,
            amount=course.price if hasattr(course, "price") else 1000,
            payment_method="transfer",
            stripe_session_id=session_data["session_id"],
            stripe_price_id=price_id,
            stripe_product_id=product_id,
        )

        return Response(
            {
                **session_data,
                "payment_id": payment.id,
                "message": "Ссылка для оплаты создана",
            }
        )


class PaymentSuccessAPIView(APIView):
    """
    API для обработки успешной оплаты.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        session_id = request.query_params.get("session_id")
        course_id = request.query_params.get("course_id")

        return Response(
            {
                "success": True,
                "message": "Оплата прошла успешно!",
                "course_id": course_id,
                "session_id": session_id,
            }
        )


class PaymentCancelAPIView(APIView):
    """
    API для обработки отмены оплаты.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"success": False, "message": "Оплата отменена"})
