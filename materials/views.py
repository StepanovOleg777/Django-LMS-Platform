from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from .paginators import LessonPagination, CoursePagination


class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moderators").exists()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        """Фильтрует курсы: модераторы видят все, обычные пользователи - только свои."""
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
            return [permissions.IsAuthenticated(), IsOwner() | IsModerator()]
        else:
            return [permissions.IsAuthenticated()]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotModerator]
    pagination_class = LessonPagination

    def get_queryset(self):
        """Фильтрует уроки: модераторы видят все, обычные пользователи - только свои."""
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]

    def get_queryset(self):
        """Фильтрует уроки: модераторы видят все, обычные пользователи - только свои."""
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
