from django.test import TestCase
from .models import Location

class LocationTestCase(TestCase):
    def setUp(self):
        Location.objects.create(
            name='Test Blood Bank',
            address='123 Main St',
            location_type='blood_bank',
            latitude=40.7128,
            longitude=-74.0060,
            is_active=True
        )

    def test_location_creation(self):
        location = Location.objects.get(name='Test Blood Bank')
        self.assertEqual(location.location_type, 'blood_bank')
        self.assertTrue(location.is_active)
