from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Donor

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'

    def validate_date_of_birth(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise ValidationError("Donor must be at least 18 years old.")
        return value
