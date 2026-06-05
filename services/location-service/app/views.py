from rest_framework import viewsets
from django.db.models import Q
from .models import Location
from .serializers import LocationSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    filterset_fields = ['location_type', 'is_active']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
