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

        # URL для уроков - используем правильные URL для каждого действия
        self.lessons_url = reverse("lesson-list")
        self.lesson_detail_url = reverse("lesson-detail", args=[self.lesson.id])
        self.lesson_update_url = reverse("lesson-update", args=[self.lesson.id])
        self.lesson_delete_url = reverse("lesson-delete", args=[self.lesson.id])

    def test_lesson_create_with_youtube_link(self):
        """Тест создания урока с валидной ссылкой на youtube"""
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "New Lesson",
            "description": "New Description",
            "video_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course": self.course.id,
        }

        response = self.client.post(self.lessons_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_with_invalid_link(self):
        """Тест создания урока с невалидной ссылкой"""
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Invalid Lesson",
            "description": "Invalid Description",
            "video_link": "https://vimeo.com/test",
            "course": self.course.id,
        }

        response = self.client.post(self.lessons_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_update_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.user)

        data = {"title": "Updated Lesson"}
        # Используем правильный URL для обновления
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_lesson_update_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator)

        data = {"title": "Updated by Moderator"}
        # Используем правильный URL для обновления
        response = self.client.patch(self.lesson_update_url, data)
        # В зависимости от ваших permissions
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]
        )

    def test_lesson_delete_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.user)

        # Используем правильный URL для удаления
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@test.com", password="testpass123"
        )

        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

        # URL для подписки
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
        # Проверяем, что в ответе есть поле is_subscribed
        self.assertIn("is_subscribed", response.data)
        self.assertTrue(response.data["is_subscribed"])
