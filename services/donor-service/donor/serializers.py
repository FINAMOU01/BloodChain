from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Donor, Appointment

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


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate_donor_email(self, value):
        if not Donor.objects.filter(email=value).exists():
            raise ValidationError("A registered donor with this email does not exist.")
        return value

    def validate_appointment_date(self, value):
        if not self.instance and value < date.today():
            raise ValidationError("Appointment date cannot be in the past.")
        return value
