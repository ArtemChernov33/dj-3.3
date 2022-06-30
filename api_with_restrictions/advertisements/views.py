import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from .permissions import IsOwner

from django_filters import rest_framework as filters
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permissions import IsOwner


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
     #permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend,]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    filterset_fields = ['status', 'created_at']

    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object().creator:
            return Response('У вас нет прав')
        return super().destroy(request, **kwargs)

class AdvertisementFilter(filters.FilterSet):
    class Meta:
        model = Advertisement
        fields = ['status', 'created_at']
        # status = filters.NumberFilter(field_name=)
        # created_at = filters.NumberFilter()



