from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    title = models.CharField(_('название'), max_length=200)
    preview = models.ImageField(_('превью'), upload_to='courses/', blank=True, null=True)
    description = models.TextField(_('описание'))
    created_at = models.DateTimeField(_('дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата обновления'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курсы')


class Lesson(models.Model):
    title = models.CharField(_('название'), max_length=200)
    description = models.TextField(_('описание'))
    preview = models.ImageField(_('превью'), upload_to='lessons/', blank=True, null=True)
    video_link = models.URLField(_('ссылка на видео'))
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name=_('курс')
    )
    created_at = models.DateTimeField(_('дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('дата обновления'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Урок')
        verbose_name_plural = _('Уроки')
        ordering = ['created_at']