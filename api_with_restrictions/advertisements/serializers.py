from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'creator',
                  'status', 'created_at', ]

    def create(self, validated_data):
        """Метод для создания"""
        print(validated_data)
        validated_data["creator"] = self.context["request"].user
        """Кто создал сообщение"""
        print(validated_data["creator"])
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if Advertisement.objects.filter(creator=self.context["request"].user).count() > 10:
            raise Exception('Привышен лимит открытых сообщений')
        return data
