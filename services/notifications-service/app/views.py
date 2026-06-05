from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import NotificationSerializer
from .models import Notification
from metrics.exporters import EMERGENCY_ALERTS_SENT

class EmergencyAlertView(APIView):
    @swagger_auto_schema(
        request_body=NotificationSerializer,
        operation_description='Send an emergency blood alert notification.',
        responses={201: NotificationSerializer, 400: 'Validation error'}
    )
    def post(self, request):
        from .tasks import send_emergency_alert, send_push_notification
        
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save(is_emergency=True)
            EMERGENCY_ALERTS_SENT.inc()
            send_emergency_alert(notification.id)
            send_push_notification(notification.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationListView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
