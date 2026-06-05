from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Donor, Appointment
from .serializers import DonorSerializer, AppointmentSerializer

class DonorCreateView(APIView):
    @swagger_auto_schema(
        request_body=DonorSerializer,
        operation_description='Register a new blood donor. Donor must be 18 or older.',
        responses={201: DonorSerializer, 400: 'Validation error'}
    )
    def post(self, request):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonorProfileView(APIView):
    def get(self, request, email):
        try:
            donor = Donor.objects.get(email=email)
            return Response(DonorSerializer(donor).data)
        except Donor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DonorListView(APIView):
    def get(self, request):
        blood_type = request.query_params.get('blood_type')
        eligible = request.query_params.get('eligible')
        donors = Donor.objects.all()
        if blood_type:
            donors = donors.filter(blood_type=blood_type.upper())
        if eligible:
            donors = donors.filter(is_eligible=(eligible.lower() == 'true'))
        serializer = DonorSerializer(donors, many=True)
        return Response(serializer.data)

class AppointmentListView(APIView):
    def get(self, request, donor_email):
        appointments = Appointment.objects.filter(donor_email=donor_email)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class AppointmentCreateView(APIView):
    @swagger_auto_schema(
        request_body=AppointmentSerializer,
        operation_description='Create a new appointment for a donor.',
        responses={201: AppointmentSerializer, 400: 'Validation error'}
    )
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentUpdateView(APIView):
    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonorUpdateView(APIView):
    @swagger_auto_schema(
        request_body=DonorSerializer,
        operation_description='Update donor profile fields. Partial updates supported.',
        responses={200: DonorSerializer, 400: 'Validation error', 404: 'Donor not found'}
    )
    def patch(self, request, email):
        try:
            donor = Donor.objects.get(email=email)
        except Donor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DonorSerializer(donor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonorEligibilityView(APIView):
    def get(self, request, donor_email):
        try:
            donor = Donor.objects.get(email=donor_email)
        except Donor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        completed = Appointment.objects.filter(
            donor_email=donor_email,
            status='completed'
        ).order_by('-appointment_date').first()

        today = date.today()
        MIN_DONATION_GAP_DAYS = 56

        if completed:
            last_donation = completed.appointment_date
            days_since = (today - last_donation).days
            next_eligible = last_donation + timedelta(days=MIN_DONATION_GAP_DAYS)
            is_eligible = days_since >= MIN_DONATION_GAP_DAYS
            days_until_next = max(0, MIN_DONATION_GAP_DAYS - days_since)
        else:
            last_donation = None
            next_eligible = today
            is_eligible = True
            days_until_next = 0

        return Response({
            "is_eligible": is_eligible,
            "last_donation_date": last_donation.isoformat() if last_donation else None,
            "next_eligible_date": next_eligible.isoformat(),
            "days_until_next": days_until_next,
            "total_donations": Appointment.objects.filter(donor_email=donor_email, status='completed').count(),
            "blood_type": donor.blood_type,
            "age": today.year - donor.date_of_birth.year - ((today.month, today.day) < (donor.date_of_birth.month, donor.date_of_birth.day)),
        })
