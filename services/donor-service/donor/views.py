from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Donor
from .serializers import DonorSerializer

class DonorCreateView(APIView):
    @swagger_auto_schema(request_body=DonorSerializer)
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
