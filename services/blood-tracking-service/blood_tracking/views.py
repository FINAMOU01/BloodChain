from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import BloodBag
from .serializers import BloodBagSerializer

class BloodBagCreateView(APIView):
    @swagger_auto_schema(
        request_body=BloodBagSerializer,
        operation_description='Record a new blood bag collection.',
        responses={201: BloodBagSerializer, 400: 'Validation error'}
    )
    def post(self, request):
        serializer = BloodBagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='collected')
            return Response({'bag_id': serializer.instance.bag_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BloodBagDetailView(APIView):
    def get(self, request, bag_id):
        try:
            bag = BloodBag.objects.get(bag_id=bag_id)
            return Response(BloodBagSerializer(bag).data)
        except BloodBag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class BloodBagDonorListView(APIView):
    def get(self, request, donor_email):
        bags = BloodBag.objects.filter(donor_email=donor_email).order_by('-collected_at')
        serializer = BloodBagSerializer(bags, many=True)
        return Response(serializer.data)
