from rest_framework import viewsets
from .models import DonationStat, HospitalDemand
from .serializers import DonationStatSerializer, HospitalDemandSerializer

class DonationStatViewSet(viewsets.ModelViewSet):
    queryset = DonationStat.objects.all()
    serializer_class = DonationStatSerializer
    filterset_fields = ['date', 'blood_type', 'region']
    search_fields = ['region', 'blood_type']
    ordering_fields = ['date', 'total_donations']
    ordering = ['-date']


class HospitalDemandViewSet(viewsets.ModelViewSet):
    queryset = HospitalDemand.objects.all()
    serializer_class = HospitalDemandSerializer
    filterset_fields = ['date', 'hospital_id', 'blood_type']
    search_fields = ['hospital_id', 'blood_type']
    ordering_fields = ['date', 'units_needed']
    ordering = ['-date']
