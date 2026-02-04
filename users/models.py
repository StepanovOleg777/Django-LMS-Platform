from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(DjangoUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField(_('телефон'), max_length=15, blank=True, null=True)
    city = models.CharField(_('город'), max_length=100, blank=True, null=True)
    avatar = models.ImageField(_('аватар'), upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return self.email


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', _('Наличные')
        TRANSFER = 'transfer', _('Перевод на счет')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('пользователь')
    )
    payment_date = models.DateTimeField(_('дата оплаты'), auto_now_add=True)
    paid_course = models.ForeignKey(
        'materials.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('оплаченный курс')
    )
    paid_lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('оплаченный урок')
    )
    amount = models.DecimalField(_('сумма оплаты'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        _('способ оплаты'),
        max_length=10,
        choices=PaymentMethod.choices
    )

    # Stripe fields
    stripe_session_id = models.CharField(
        _('ID сессии Stripe'),
        max_length=255,
        blank=True,
        null=True
    )
    stripe_price_id = models.CharField(
        _('ID цены Stripe'),
        max_length=255,
        blank=True,
        null=True
    )
    stripe_product_id = models.CharField(
        _('ID продукта Stripe'),
        max_length=255,
        blank=True,
        null=True
    )
    payment_status = models.CharField(
        _('статус оплаты'),
        max_length=50,
        default='pending'
    )

    class Meta:
        verbose_name = _('платеж')
        verbose_name_plural = _('платежи')
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.payment_date}"