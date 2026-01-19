import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    paid_course = django_filters.NumberFilter(field_name='paid_course__id')
    paid_lesson = django_filters.NumberFilter(field_name='paid_lesson__id')
    payment_method = django_filters.ChoiceFilter(choices=Payment.PaymentMethod.choices)

    ordering = django_filters.OrderingFilter(
        fields=(
            ('payment_date', 'payment_date'),
        )
    )

    class Meta:
        model = Payment
        fields = ['paid_course', 'paid_lesson', 'payment_method']