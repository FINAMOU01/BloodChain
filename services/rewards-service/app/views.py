from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Reward, Redemption
from .serializers import RewardSerializer, RedemptionSerializer
from metrics.exporters import REWARDS_MINTED

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    filterset_fields = ['donor_id']
    search_fields = ['donor_id', 'reason']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        REWARDS_MINTED.inc()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RedemptionViewSet(viewsets.ModelViewSet):
    queryset = Redemption.objects.all()
    serializer_class = RedemptionSerializer
    filterset_fields = ['donor_id']
    search_fields = ['donor_id', 'reward']
