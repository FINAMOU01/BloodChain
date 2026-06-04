from rest_framework import viewsets
from .models import Reward, Redemption
from .serializers import RewardSerializer, RedemptionSerializer

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    filterset_fields = ['donor_id']
    search_fields = ['donor_id', 'reason']


class RedemptionViewSet(viewsets.ModelViewSet):
    queryset = Redemption.objects.all()
    serializer_class = RedemptionSerializer
    filterset_fields = ['donor_id']
    search_fields = ['donor_id', 'reward']
