from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import YoutubeURLValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            YoutubeURLValidator(field="video_link"),
            serializers.UniqueTogetherValidator(
                queryset=Lesson.objects.all(),
                fields=["title", "course"],
                message="Урок с таким названием уже существует в этом курсе",
            ),
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ("user",)


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source="lessons.count", read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "owner",
            "created_at",
            "updated_at",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]
        read_only_fields = ("owner", "created_at", "updated_at")

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user, course=obj, is_active=True
            ).exists()
        return False

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
