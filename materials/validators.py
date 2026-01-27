from rest_framework import serializers
from urllib.parse import urlparse


class YoutubeURLValidator:
    """
    Валидатор для проверки, что ссылка ведет только на youtube.com
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field) if isinstance(value, dict) else value
        if url:
            parsed_url = urlparse(url)
            if parsed_url.netloc not in ["youtube.com", "www.youtube.com"]:
                raise serializers.ValidationError(
                    f"Допустимы только ссылки на youtube.com. Получена ссылка: {parsed_url.netloc}"
                )
