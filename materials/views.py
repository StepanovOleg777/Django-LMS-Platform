from rest_framework import viewsets, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, LessonForCourseSerializer
from users.permissions import IsModerator, IsOwner


class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moderators").exists()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
