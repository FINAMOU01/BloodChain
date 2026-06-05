from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Hospital, BloodRequest, BloodStock
from .serializers import HospitalSerializer, BloodRequestSerializer, BloodStockSerializer
from metrics.exporters import BLOOD_REQUESTS_CREATED

class HospitalCreateView(APIView):
    @swagger_auto_schema(
        request_body=HospitalSerializer,
        operation_description='Register a new hospital.',
        responses={201: HospitalSerializer, 400: 'Validation error'}
    )
    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HospitalProfileView(APIView):
    def get(self, request, email):
        try:
            hospital = Hospital.objects.get(email=email)
            return Response(HospitalSerializer(hospital).data)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class HospitalUpdateView(APIView):
    @swagger_auto_schema(
        request_body=HospitalSerializer,
        operation_description='Update hospital profile details. Partial updates supported.',
        responses={200: HospitalSerializer, 400: 'Validation error', 404: 'Hospital not found'}
    )
    def patch(self, request, email):
        try:
            hospital = Hospital.objects.get(email=email)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HospitalSerializer(hospital, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            BLOOD_REQUESTS_CREATED.inc()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BloodRequestListView(APIView):
    def get(self, request):
        requests = BloodRequest.objects.all()
        serializer = BloodRequestSerializer(requests, many=True)
        return Response(serializer.data)

class BloodRequestDetailView(APIView):
    def get(self, request, pk):
        try:
            req = BloodRequest.objects.get(pk=pk)
            return Response(BloodRequestSerializer(req).data)
        except BloodRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class BloodRequestUpdateView(APIView):
    @swagger_auto_schema(
        request_body=BloodRequestSerializer,
        operation_description='Update blood request status or details. Partial updates supported.',
        responses={200: BloodRequestSerializer, 400: 'Validation error', 404: 'Blood request not found'}
    )
    def patch(self, request, pk):
        try:
            req = BloodRequest.objects.get(pk=pk)
        except BloodRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BloodRequestSerializer(req, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BloodStockView(APIView):
    def get(self, request, hospital_id):
        stock = BloodStock.objects.filter(hospital_id=hospital_id)
        serializer = BloodStockSerializer(stock, many=True)
        return Response(serializer.data)

class BloodStockUpdateView(APIView):
    @swagger_auto_schema(
        request_body=BloodStockSerializer,
        operation_description='Update or create a blood stock entry for a hospital.',
        responses={200: BloodStockSerializer, 400: 'Validation error'}
    )
    def post(self, request, hospital_id):
        blood_type = request.data.get('blood_type')
        units = request.data.get('units_available')
        try:
            stock = BloodStock.objects.get(hospital_id=hospital_id, blood_type=blood_type)
            stock.units_available = units
            stock.save()
        except BloodStock.DoesNotExist:
            stock = BloodStock.objects.create(
                hospital_id=hospital_id,
                blood_type=blood_type,
                units_available=units
            )
        return Response(BloodStockSerializer(stock).data)
