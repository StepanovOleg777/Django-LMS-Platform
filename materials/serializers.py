from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока."""

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')


class LessonForCourseSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор уроков для встраивания в курс."""

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link']


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса с уроками и их количеством."""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonForCourseSerializer(many=True, read_only=True)  # <-- Используем отдельный сериализатор

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'created_at', 'updated_at', 'lessons_count', 'lessons']
        read_only_fields = ('created_at', 'updated_at')

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе."""
        return obj.lessons.count()