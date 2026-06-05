from rest_framework import serializers
from .models import BloodBag

class BloodBagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBag
        fields = '__all__'
        read_only_fields = ['bag_id', 'blockchain_tx_hash', 'collected_at', 'last_updated']
