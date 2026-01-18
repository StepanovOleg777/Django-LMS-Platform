from django.contrib import admin
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'description', 'video_link', 'preview')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    inlines = [LessonInline]

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'updated_at')
    list_filter = ('course', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'video_link')
    raw_id_fields = ('course',)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'