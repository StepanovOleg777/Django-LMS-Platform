import stripe
from django.conf import settings
from .models import Course

# Настройка Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    """
    Создает продукт в Stripe.
    """
    try:
        product = stripe.Product.create(
            name=course.title,
            description=course.description[:500] if course.description else "Курс",
        )
        return product.id
    except stripe.error.StripeError as e:
        print(f"Ошибка создания продукта в Stripe: {e}")
        return None


def create_stripe_price(course, product_id):
    """
    Создает цену в Stripe.
    Цена указывается в копейках (центы).
    """
    # Предполагаем, что курс имеет поле price или используем фиксированную цену
    # Если у курса нет цены, используем 1000 рублей (100000 копеек)
    amount = getattr(course, "price", 1000) * 100  # переводим в копейки

    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount,  # в копейках
            currency="rub",  # рубли
        )
        return price.id
    except stripe.error.StripeError as e:
        print(f"Ошибка создания цены в Stripe: {e}")
        return None


def create_stripe_session(price_id, course_id, user_email):
    """
    Создает сессию оплаты в Stripe.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{settings.DOMAIN}/api/payments/success/?course_id={course_id}",
            cancel_url=f"{settings.DOMAIN}/api/payments/cancel/",
            customer_email=user_email,
            metadata={
                "course_id": str(course_id),
            },
        )
        return {
            "session_id": session.id,
            "url": session.url,
            "payment_status": session.payment_status,
        }
    except stripe.error.StripeError as e:
        print(f"Ошибка создания сессии в Stripe: {e}")
        return None
