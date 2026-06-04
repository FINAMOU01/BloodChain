from rest_framework import serializers
from .models import Reward, Redemption

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'donor_id', 'points', 'reason', 'created_at']
        read_only_fields = ['id', 'created_at']


class RedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redemption
        fields = ['id', 'donor_id', 'reward', 'redeemed_at']
        read_only_fields = ['id', 'redeemed_at']
