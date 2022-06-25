from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        user = self.context["request"].user
        status_open = Advertisement.objects.filter(creator_id=user.id).filter(status='OPEN').count
        request_method = self.context["request"].method
        if (request_method == 'POST' or data["status"] == 'OPEN') and status_open > 10:
        # if Advertisement.objects.filter(creator=self.context["request"].user).count() > 10:
            raise ValidationError('Привышен лимит открытых сообщений')
        return data
