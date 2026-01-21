from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создание групп модераторов'

    def handle(self, *args, **kwargs):
        moderators_group, created = Group.objects.get_or_create(name='moderators')

        # Права для курсов
        course_content_type = ContentType.objects.get_for_model(Course)
        course_permissions = Permission.objects.filter(content_type=course_content_type)

        for perm in course_permissions:
            if perm.codename in ['view_course', 'change_course']:
                moderators_group.permissions.add(perm)

        # Права для уроков
        lesson_content_type = ContentType.objects.get_for_model(Lesson)
        lesson_permissions = Permission.objects.filter(content_type=lesson_content_type)

        for perm in lesson_permissions:
            if perm.codename in ['view_lesson', 'change_lesson']:
                moderators_group.permissions.add(perm)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "moderators" создана'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "moderators" обновлена'))