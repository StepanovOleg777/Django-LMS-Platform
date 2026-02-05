from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, SubscriptionAPIView, LessonViewSet
from materials.payments_views import (
    CreatePaymentAPIView,
    PaymentSuccessAPIView,
    PaymentCancelAPIView,
)
from users.views import UserViewSet, PaymentViewSet, UserRegisterAPIView

# Настройка схемы для документации
schema_view = get_schema_view(
    openapi.Info(
        title="Django LMS Platform API",
        default_version="v1",
        description="API для системы управления обучением (LMS)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@lms.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentViewSet)
router.register(r"lessons", LessonViewSet)

urlpatterns = [
    # Документация Swagger UI
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # Документация в ReDoc
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Документация в JSON/YAML
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger.yaml/", schema_view.without_ui(cache_timeout=0), name="schema-yaml"),
    # Админка
    path("admin/", admin.site.urls),
    # API
    path("api/", include(router.urls)),
    # URL для подписок
    path("api/subscriptions/", SubscriptionAPIView.as_view(), name="subscription"),
    # Платежи Stripe
    path("api/payments/create/", CreatePaymentAPIView.as_view(), name="create-payment"),
    path(
        "api/payments/success/", PaymentSuccessAPIView.as_view(), name="payment-success"
    ),
    path("api/payments/cancel/", PaymentCancelAPIView.as_view(), name="payment-cancel"),
    # JWT токены
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Регистрация
    path("api/register/", UserRegisterAPIView.as_view(), name="register"),
]

# Статические и медиа файлы для разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
