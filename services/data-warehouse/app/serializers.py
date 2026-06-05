from rest_framework import serializers
from .models import DonationStat, HospitalDemand

class DonationStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationStat
        fields = ['id', 'date', 'total_donations', 'blood_type', 'region', 'created_at']
        read_only_fields = ['id', 'created_at']


class HospitalDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalDemand
        fields = ['id', 'date', 'hospital_id', 'blood_type', 'units_needed', 'created_at']
        read_only_fields = ['id', 'created_at']
