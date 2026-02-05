from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    title = models.CharField(_("название"), max_length=200)
    preview = models.ImageField(
        _("превью"), upload_to="courses/", blank=True, null=True
    )
    description = models.TextField(_("описание"))
    price = models.DecimalField(
        _("цена"), max_digits=10, decimal_places=2, default=0.00, blank=True, null=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("владелец"),
    )
    created_at = models.DateTimeField(_("дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("дата обновления"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("курс")
        verbose_name_plural = _("курсы")


class Lesson(models.Model):
    title = models.CharField(_("название"), max_length=200)
    description = models.TextField(_("описание"))
    preview = models.ImageField(
        _("превью"), upload_to="lessons/", blank=True, null=True
    )
    video_link = models.URLField(_("ссылка на видео"))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name=_("курс")
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("владелец"),
    )
    created_at = models.DateTimeField(_("дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("дата обновления"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("урок")
        verbose_name_plural = _("уроки")


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("пользователь"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("курс"),
    )
    is_active = models.BooleanField(_("активная подписка"), default=True)
    created_at = models.DateTimeField(_("дата подписки"), auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        verbose_name = _("подписка")
        verbose_name_plural = _("подписки")

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
