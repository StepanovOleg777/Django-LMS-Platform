from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, SubscriptionAPIView
from users.views import UserViewSet, PaymentViewSet, UserRegisterAPIView
from materials.views import (
    LessonListCreateAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # URL для уроков
    path("api/lessons/", LessonListCreateAPIView.as_view(), name="lesson-list"),
    path(
        "api/lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"
    ),
    path(
        "api/lessons/<int:pk>/update/",
        LessonUpdateAPIView.as_view(),
        name="lesson-update",
    ),
    path(
        "api/lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lesson-delete",
    ),
    # URL для подписок
    path(
        "api/lessons/subscription/", SubscriptionAPIView.as_view(), name="subscription"
    ),
    # JWT токены
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Регистрация
    path("api/register/", UserRegisterAPIView.as_view(), name="register"),
]
