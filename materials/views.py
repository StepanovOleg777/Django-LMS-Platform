from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from .paginators import LessonPagination, CoursePagination
from .tasks import send_course_update_email  # Импорт задачи Celery


class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moderators").exists()


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return request.user.groups.filter(name="moderators").exists()


class CourseViewSet(viewsets.ModelViewSet):
    """
    API для работы с курсами.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    @swagger_auto_schema(
        operation_description="Получить список курсов с пагинацией",
        responses={200: CourseSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый курс",
        request_body=CourseSerializer,
        responses={201: CourseSerializer, 400: "Некорректные данные"},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить детальную информацию о курсе",
        responses={200: CourseSerializer, 404: "Курс не найден"},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить курс",
        request_body=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: "Некорректные данные",
            403: "Нет прав доступа",
            404: "Курс не найден",
        },
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        # Если обновление успешно, запускаем задачу отправки писем
        if response.status_code == 200:
            course_id = kwargs.get("pk")
            send_course_update_email.delay(course_id)

        return response

    @swagger_auto_schema(
        operation_description="Частично обновить курс",
        request_body=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: "Некорректные данные",
            403: "Нет прав доступа",
            404: "Курс не найден",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)

        # Если обновление успешно, запускаем задачу отправки писем
        if response.status_code == 200:
            course_id = kwargs.get("pk")
            send_course_update_email.delay(course_id)

        return response

    @swagger_auto_schema(
        operation_description="Удалить курс",
        responses={204: "Курс удален", 403: "Нет прав доступа", 404: "Курс не найден"},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        """Фильтрует курсы: модераторы видят все, обычные пользователи - только свои."""
        # Исправление для Swagger документации
        if getattr(self, "swagger_fake_view", False):
            return Course.objects.none()

        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Устанавливает владельца при создании курса."""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsNotModerator()]
        elif self.action == "destroy":
            return [permissions.IsAuthenticated(), IsOwner()]
        elif self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated(), IsOwnerOrModerator()]
        else:
            return [permissions.IsAuthenticated()]


class LessonViewSet(viewsets.ModelViewSet):
    """
    API для работы с уроками.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination

    @swagger_auto_schema(
        operation_description="Получить список уроков с пагинацией",
        responses={200: LessonSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый урок",
        request_body=LessonSerializer,
        responses={201: LessonSerializer, 400: "Некорректные данные"},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить детальную информацию об уроке",
        responses={200: LessonSerializer, 404: "Урок не найден"},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить урок",
        request_body=LessonSerializer,
        responses={
            200: LessonSerializer,
            400: "Некорректные данные",
            403: "Нет прав доступа",
            404: "Урок не найден",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить урок",
        request_body=LessonSerializer,
        responses={
            200: LessonSerializer,
            400: "Некорректные данные",
            403: "Нет прав доступа",
            404: "Урок не найден",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить урок",
        responses={204: "Урок удален", 403: "Нет прав доступа", 404: "Урок не найден"},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        """Фильтрует уроки: модераторы видят все, обычные пользователи - только свои."""
        # Исправление для Swagger документации
        if getattr(self, "swagger_fake_view", False):
            return Lesson.objects.none()

        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Устанавливает владельца при создании урока."""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsNotModerator()]
        elif self.action == "destroy":
            return [permissions.IsAuthenticated(), IsOwner()]
        elif self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated(), IsOwnerOrModerator()]
        else:
            return [permissions.IsAuthenticated()]


class SubscriptionAPIView(APIView):
    """
    API для управления подписками на курсы.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Подписаться или отписаться от курса",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course_id"],
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID курса"
                )
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Сообщение о результате операции",
                    )
                },
            ),
            400: "Неверные данные",
            404: "Курс не найден",
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})
