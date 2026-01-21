from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from users.models import Payment, User
import decimal

User = get_user_model()


class Command(BaseCommand):
    help = "Создание тестовых платежей"

    def handle(self, *args, **kwargs):
        # Получаем существующего суперпользователя или создаем тестового
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                user = User.objects.create_user(
                    email="test_payment@example.com",
                    password="testpass123",
                    first_name="Тестовый",
                    last_name="Пользователь",
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при получении пользователя: {e}")
            )
            return

        # Получаем или создаем тестовый курс
        course, created = Course.objects.get_or_create(
            title="Python для начинающих",
            defaults={"description": "Базовый курс по Python"},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Создан курс: {course.title}"))

        # Получаем или создаем тестовый урок
        lesson, created = Lesson.objects.get_or_create(
            title="Введение в Python",
            defaults={
                "description": "Первый урок по Python",
                "video_link": "https://youtube.com/watch?v=python_intro",
                "course": course,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Создан урок: {lesson.title}"))

        # Данные для платежей
        payments_data = [
            {
                "user": user,
                "paid_course": course,
                "paid_lesson": None,
                "amount": decimal.Decimal("10000.00"),
                "payment_method": Payment.PaymentMethod.CASH,
            },
            {
                "user": user,
                "paid_course": None,
                "paid_lesson": lesson,
                "amount": decimal.Decimal("2000.00"),
                "payment_method": Payment.PaymentMethod.TRANSFER,
            },
            {
                "user": user,
                "paid_course": course,
                "paid_lesson": None,
                "amount": decimal.Decimal("15000.00"),
                "payment_method": Payment.PaymentMethod.TRANSFER,
            },
        ]

        created_count = 0
        for idx, payment_data in enumerate(payments_data, 1):
            # Проверяем, нет ли уже такого платежа
            existing_payment = Payment.objects.filter(
                user=payment_data["user"],
                amount=payment_data["amount"],
                payment_method=payment_data["payment_method"],
            ).first()

            if not existing_payment:
                payment = Payment.objects.create(**payment_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"{idx}. Создан платеж: {payment}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"{idx}. Платеж уже существует: {existing_payment}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"\nУспешно создано {created_count} новых платежей")
        )
        self.stdout.write(f"Всего платежей в базе: {Payment.objects.count()}")
