from django.db import models
from django.contrib.gis.db import models as gis_models

class Location(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('blood_bank', 'Blood Bank'),
        ('hospital', 'Hospital'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    point = gis_models.PointField(geography=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"
