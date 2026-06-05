from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    location_type_display = serializers.CharField(source='get_location_type_display', read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'location_type', 'location_type_display', 'latitude', 'longitude', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
