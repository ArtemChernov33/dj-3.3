from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from .permissions import IsOwner

from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permissions import IsOwner


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend,]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    # def get_permissions(self):
    #     """Получение прав для действий."""
    #     if self.action in ["create", "update", "partial_update", "destroy",]:
    #         return [IsAuthenticated()]
    #     return []

    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object().creator:
            return Response('У вас нет прав')
        return super().destroy(request, **kwargs)



