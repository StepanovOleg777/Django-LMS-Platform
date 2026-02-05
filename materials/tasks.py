from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from .models import Course, Subscription


@shared_task
def test_celery():
    """
    Тестовая задача для проверки работы Celery.
    """
    return "Celery работает успешно!"


@shared_task
def send_course_update_email(course_id):
    """
    Отправляет email всем подписчикам курса об обновлении.
    """
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)

        if not subscriptions.exists():
            return f"Нет активных подписчиков для курса {course.title}"

        emails = [sub.user.email for sub in subscriptions if sub.user.email]

        if not emails:
            return f"У подписчиков курса {course.title} нет email"

        subject = f"Обновление курса: {course.title}"
        message = f"""
        Здравствуйте!

        Курс "{course.title}" был обновлен.

        Новое описание: {course.description[:100]}...

        Перейдите по ссылке, чтобы увидеть изменения: 
        {settings.DOMAIN}/api/courses/{course.id}/

        С уважением,
        Команда LMS Platform
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=(
                settings.DEFAULT_FROM_EMAIL
                if hasattr(settings, "DEFAULT_FROM_EMAIL")
                else "noreply@lms.local"
            ),
            recipient_list=emails,
            fail_silently=False,
        )

        return f"Отправлено {len(emails)} писем для курса {course.title}"

    except Course.DoesNotExist:
        return f"Курс с id {course_id} не найден"
    except Exception as e:
        return f"Ошибка отправки email: {str(e)}"


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца.
    """
    User = get_user_model()

    # Дата месяц назад
    month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей, которые не заходили более месяца и еще активны
    inactive_users = User.objects.filter(
        last_login__lt=month_ago, is_active=True
    ).exclude(
        is_superuser=True  # Не блокируем суперпользователей
    )

    count = inactive_users.count()

    if count == 0:
        return "Нет неактивных пользователей для блокировки"

    # Блокируем пользователей
    inactive_users.update(is_active=False)

    # Собираем email для отчета
    emails = list(inactive_users.values_list("email", flat=True))

    # Отправляем отчет администратору (опционально)
    if hasattr(settings, "ADMIN_EMAIL") and settings.ADMIN_EMAIL:
        admin_subject = "Отчет о блокировке неактивных пользователей"
        admin_message = f"""
        Отчет о блокировке неактивных пользователей:

        Заблокировано пользователей: {count}
        Список email: {', '.join(emails)}

        Время выполнения: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

    return f"Заблокировано {count} пользователей: {', '.join(emails[:5])}{'...' if len(emails) > 5 else ''}"
