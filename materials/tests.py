from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем обычного пользователя
        self.user = User.objects.create_user(
            email="test@test.com", password="testpass123"
        )

        # Создаем модератора
        self.moderator = User.objects.create_user(
            email="moderator@test.com", password="modpass123"
        )

        # Создаем курс
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson Description",
            video_link="https://www.youtube.com/watch?v=test",
            course=self.course,
            owner=self.user,
        )

        self.lessons_url = reverse("lessons-list")
        self.lesson_detail_url = reverse("lessons-detail", args=[self.lesson.id])


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@test.com", password="testpass123"
        )

        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

        # URL для подписок - используем новое имя
        self.subscription_url = reverse("subscription")

    def test_subscription_create(self):
        """Тест создания подписки"""
        self.client.force_authenticate(user=self.user)

        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_delete(self):
        """Тест удаления подписки"""
        self.client.force_authenticate(user=self.user)

        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        # Затем удаляем ее
        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_course_with_subscription_info(self):
        """Тест получения информации о подписке в курсе"""
        self.client.force_authenticate(user=self.user)

        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        # Получаем информацию о курсе
        course_detail_url = reverse("course-detail", args=[self.course.id])
        response = self.client.get(course_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_subscribed", response.data)
        self.assertTrue(response.data["is_subscribed"])


class DocumentationTestCase(TestCase):
    def test_swagger_docs(self):
        """Тест доступности документации Swagger"""
        response = self.client.get("/swagger/")
        self.assertEqual(response.status_code, 200)

    def test_redoc_docs(self):
        """Тест доступности документации ReDoc"""
        response = self.client.get("/redoc/")
        self.assertEqual(response.status_code, 200)
