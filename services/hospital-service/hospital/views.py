from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import BloodRequest, BloodStock
from .serializers import BloodRequestSerializer, BloodStockSerializer

class BloodRequestCreateView(APIView):
    @swagger_auto_schema(
        request_body=BloodRequestSerializer,
        operation_description='Create a new blood request.',
        responses={201: BloodRequestSerializer, 400: 'Validation error'}
    )
    def post(self, request):
        serializer = BloodRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status='pending')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BloodRequestListView(APIView):
    def get(self, request):
        requests = BloodRequest.objects.all()
        serializer = BloodRequestSerializer(requests, many=True)
        return Response(serializer.data)

class BloodStockView(APIView):
    def get(self, request, hospital_id):
        stock = BloodStock.objects.filter(hospital_id=hospital_id)
        serializer = BloodStockSerializer(stock, many=True)
        return Response(serializer.data)
